import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head'


// import logo from './assets/logo.png'


export default function Appd() {
    const containerRef = useRef(null);
    const gameRef = useRef(null);
    const [game, setGame] = useState();
    const [gameConfig, setGameConfig] = useState();


    var map;
    var text;
    var sx = 0;
    var sy = 0;
    var mapWidth = 51;
    var mapHeight = 37;
    var distance = 0;
    var tiles = [7, 7, 7, 6, 6, 6, 0, 0, 0, 1, 1, 2, 3, 4, 5];
    var cursors;
    var controls;
    var bug;


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

        wallLayer.setCollisionByProperty({ collides: true });

        var frameRate = 15;

        const spawnPoint = map.findObject("Objects", obj => obj.name === "Spawn Point");
        bug = this.physics.add.sprite(spawnPoint.x, spawnPoint.y, 'crawl', 'up0000.png');

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
                    height: 300,
                    scene: {
                        preload: preload,
                        create: create,
                        update: update
                    },
                    physics: {
                        default: "arcade",
                        arcade: {
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
