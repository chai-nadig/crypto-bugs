import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head'


export default function Appd() {
    const containerRef = useRef(null);
    const gameRef = useRef(null);
    const [game, setGame] = useState();
    const [gameConfig, setGameConfig] = useState();

    var map;
    var cursors;
    var controls;
    var bug;

    function shuffle(array) {
        let currentIndex = array.length, randomIndex;

        // While there remain elements to shuffle...
        while (currentIndex != 0) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;

            // And swap it with the current element.
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex], array[currentIndex]];
        }
        return array;
    }

    function arrayEquals(a, b) {
        return Array.isArray(a) &&
            Array.isArray(b) &&
            a.length === b.length &&
            a.every((val, index) => val === b[index]);
    }

    function explore(grid, wallTileID, i, j) {
        let directions = [
            [0, 1],  // Right
            [0, -1], // Left
            [1, 0],  // Down
            [-1, 0], // Up
        ];

        if (grid[i][j] == 0) {
            return
        }

        grid[i][j] = 0;

        for (var d in shuffle(directions)) {
            let dir = directions[d];

            let pi = i + dir[0];
            let pj = j + dir[1];
            if (isViableCell(pi, pj, grid, dir, wallTileID)) {
                explore(grid, wallTileID, pi, pj );
            }
        }
    }

    function isViableCell(i, j, grid, direction, wallTileID) {
        const m = grid.length
        const n = grid[0].length

        if (i < 0 || j < 0 || i >= m || j >= n) {
            return false;
        }

        if (grid[i][j] == 0) {
            return false;
        }

        var cellsToCheck = [];
        if (arrayEquals(direction, [0, 1])) {
            cellsToCheck = [
                [i - 1, j],
                [i + 1, j],
                [i - 1, j + 1],
                [i + 1, j + 1],
            ];
        } else if (arrayEquals(direction, [0, -1])) {
            cellsToCheck = [
                [i - 1, j],
                [i + 1, j],
                [i - 1, j - 1],
                [i + 1, j - 1],
            ];
        } else if (arrayEquals(direction, [1, 0])) {
            cellsToCheck = [
                [i, j - 1],
                [i, j + 1],
                [i + 1, j - 1],
                [i + 1, j + 1],
            ];
        } else if (arrayEquals(direction, [-1, 0])) {
            cellsToCheck = [
                [i, j - 1],
                [i, j + 1],
                [i - 1, j - 1],
                [i - 1, j + 1],
            ];
        }

        let countWalls = 0;
        for (var c in cellsToCheck) {
            let cell = cellsToCheck[c];
            if (isWall(cell[0], cell[1], grid, wallTileID)) {
                countWalls += 1;
            }
        }

        return countWalls == 4;
    }

    function isWall(i, j, grid, wallTileID) {
        const m = grid.length
        const n = grid[0].length

        if (i < 0 || j < 0 || i >= m || j >= n) {
            return true;
        }

        if (grid[i][j] == wallTileID) {
            return true;
        }
        return false;
    }


    function generateMaze(map, layer, wallTileID) {
        // m rows, n columns
        const m = layer.layer.height;
        const n = layer.layer.width;

        let grid = [];
        for (let i = 0; i < m-2; i++) {
            let row = []
            for (let j = 0; j < n-2; j++) {
                row.push(wallTileID);
            }
            grid.push(row);
        }

        grid[0][0] = 0;

        explore(grid, wallTileID, m-3, n-3 );

        for (let i = 1; i < m-1; i++) {
            for (let j = 1; j < n-1; j++) {
                if (grid[i - 1][j - 1] != wallTileID) {
                    continue
                }

                let oldTile = layer.layer.data[i][j];
                let newTile = new Phaser.Tilemaps.Tile(oldTile.layer, wallTileID, oldTile.x, oldTile.y, oldTile.width, oldTile.height, oldTile.baseWidth, oldTile.baseHeight);
                newTile.properties['collides'] = true;
                map.putTileAt(newTile, oldTile.x, oldTile.y, true, "Walls");
            }
        }
    }

    function preload() {
        this.load.image("tiles", "../images/outdoor-tileset.png");
        this.load.tilemapTiledJSON("map", "../assets/empty-maze.json");
        this.load.multiatlas('crawl', '../assets/crawl.json', '../images/crawl');
    }

    function create() {
        map = this.make.tilemap({ key: "map" });
        var tileset = map.addTilesetImage("outdoor tileset", "tiles");

        var grassLayer = map.createLayer("Grass", tileset, 0, 0);
        var wallLayer = map.createLayer("Walls", tileset, 0, 0);

        generateMaze(map, wallLayer, 77);

        wallLayer.setCollisionByProperty({ collides: true });
        
        console.log(wallLayer);

        var frameRate = 15;

        const spawnPoint = map.findObject("Objects", obj => obj.name === "Spawn Point");
        bug = this.physics.add.sprite(spawnPoint.x, spawnPoint.y, 'crawl', 'up0000.png');
        bug.body.setCircle(9, 3, 3);

        this.physics.add.collider(bug, wallLayer);

        var crawlUpFrames = this.anims.generateFrameNames('crawl', {
            start: 0, end: 3, zeroPad: 4, prefix: 'up', suffix: '.png',
        })

        this.anims.create({ key: 'crawl-up', frames: crawlUpFrames, frameRate: frameRate, repeat: -1 });
        bug.anims.play('crawl-up');

        var crawlDownFrames = this.anims.generateFrameNames('crawl', {
            start: 0, end: 3, zeroPad: 4, prefix: 'down', suffix: '.png',
        })
        this.anims.create({ key: 'crawl-down', frames: crawlDownFrames, frameRate: frameRate, repeat: -1 });

        var crawlRightFrames = this.anims.generateFrameNames('crawl', {
            start: 0, end: 3, zeroPad: 4, prefix: 'right', suffix: '.png',
        })
        this.anims.create({ key: 'crawl-right', frames: crawlRightFrames, frameRate: frameRate, repeat: -1 });


        var crawlLeftFrames = this.anims.generateFrameNames('crawl', {
            start: 0, end: 3, zeroPad: 4, prefix: 'left', suffix: '.png',
        })
        this.anims.create({ key: 'crawl-left', frames: crawlLeftFrames, frameRate: frameRate, repeat: -1 });


        // Phaser supports multiple cameras, but you can access the default camera like this:
        const camera = this.cameras.main;

        camera.startFollow(bug);
        // Constrain the camera so that it isn't allowed to move outside the width/height of tilemap
        camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

        camera.setZoom(1.5);

        // Set up the arrows to control the camera
        cursors = this.input.keyboard.createCursorKeys();
        controls = new Phaser.Cameras.Controls.FixedKeyControl({
            camera: camera,
            left: cursors.left,
            right: cursors.right,
            up: cursors.up,
            down: cursors.down,
            speed: 0.5
        });
    }


    function update(time, delta) {
        const speed = 150;
        const prevVelocity = bug.body.velocity.clone(); 

        // Stop any previous movement from the last frame
        bug.body.setVelocity(0);

        // Horizontal movement
        if (cursors.left.isDown) {
            bug.body.setVelocityX(-speed);
        } else if (cursors.right.isDown) {
            bug.body.setVelocityX(speed);
        }

        // Vertical movement
        if (cursors.up.isDown) {
            bug.body.setVelocityY(-speed);
        } else if (cursors.down.isDown) {
            bug.body.setVelocityY(speed);
        }

        // Normalize and scale the velocity so that bug can't move faster along a diagonal
        bug.body.velocity.normalize().scale(speed);


        // Update the animation last and give left/right animations precedence over up/down animations
        if (cursors.left.isDown) {
            bug.anims.play("crawl-left", true);
        } else if (cursors.right.isDown) {
            bug.anims.play("crawl-right", true);
        } else if (cursors.up.isDown) {
            bug.anims.play("crawl-up", true);
        } else if (cursors.down.isDown) {
            bug.anims.play("crawl-down", true);
        } else {
            bug.anims.stop();
        }

        controls.update(delta);
    }



    useEffect(() => {
        if (!game && containerRef.current) {
            import('phaser').then(({ Game }) => {
                setGameConfig({
                    type: Phaser.AUTO,
                    width: 800,
                    height: 800,
                    scene: {
                        preload: preload,
                        create: create,
                        update: update
                    },
                    physics: {
                        default: "arcade",
                        arcade: {
                            debug: true,
                            gravity: { y: 0 }
                        }
                    }
                });

                const newGame = new Game({
                    ...gameConfig,
                    parent: containerRef.current,
                });

                setGame(newGame);
            });
        }
        return () => {
            game?.destroy(true);
        };
    }, [containerRef, game, gameConfig]);

    return (
        <div id="bodyy" className="flex flex-col items-center justify-center min-h-screen py-2">
            <Head>
                <title>crypto-bugs</title>
                <link rel="icon" href="/images/favicon.png" />
                <meta property="og:title" content="crypto-bugs" key="ogtitle" />
                <meta property="og:description" content="An NFT loveliness of 11,111 ladybugs" key="ogdesc" />
                <meta property="og:type" content="website" key="ogtype" />
                <meta property="og:url" content="https://crypto-bugs.com/" key="ogurl" />
                <meta property="og:image" content="https://crypto-bugs.com/images/favicon.png" key="ogimage" />
                <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
                <meta name="twitter:card" content="summary_large_image" key="twcard" />
                <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
                <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
                <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
                <meta name="twitter:description" content="An NFT loveliness of 11,111 ladybugs" key="twdesc" />
                <meta name="twitter:image" content="https://crypto-bugs.com/images/favicon.png" key="twimage" />
                <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu+Mono" />
            </Head>
            <h1 className="p-10 text-5xl text-crypto-red">
                <a href="/">crypto-bugs</a>
            </h1>
            <div id="tbContainer" ref={containerRef}></div>
        </div>
    );
}
