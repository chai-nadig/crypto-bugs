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


    function preload() {
        this.load.setBaseURL('http://labs.phaser.io');  
        this.load.image('tiles', 'assets/tilemaps/tiles/muddy-ground.png');
        this.load.bitmapFont('nokia16', 'assets/fonts/bitmap/nokia16.png', 'assets/fonts/bitmap/nokia16.xml');
    }

    function create() {
        var mapData = [];

        for (var y = 0; y < mapHeight; y++) {
            var row = [];

            for (var x = 0; x < mapWidth; x++) {
                //  Scatter the tiles so we get more mud and less stones
                var tileIndex = Phaser.Math.RND.weightedPick(tiles);

                row.push(tileIndex);
            }

            mapData.push(row);
        }

        map = this.make.tilemap({ data: mapData, tileWidth: 16, tileHeight: 16 });

        var tileset = map.addTilesetImage('tiles');
        var layer = map.createLayer(0, tileset, 0, 0);

        text = this.add.bitmapText(10, 50, 'nokia16').setScrollFactor(0);
    }


    function update(time, delta) {
        //  Any speed as long as 16 evenly divides by it
        sx += 0.5;

        distance += sx;

        text.setText("Distance: " + distance + 'px');

        if (sx === 16) {  // (sx === 16) {
            //  Reset and create new strip

            var tile;
            var prev;

            for (var y = 0; y < mapHeight; y++) {
                for (var x = 1; x < mapWidth; x++) {
                    tile = map.getTileAt(x, y);
                    prev = map.getTileAt(x - 1, y);

                    prev.index = tile.index;

                    if (x === mapWidth - 1) {
                        tile.index = Phaser.Math.RND.weightedPick(tiles);
                    }
                }
            }

            // for (var x = 0; y < mapWidth; x++) {
            //     for (var y = 1; x < mapHeight; y++) {
            //         tile = map.getTileAt(x, y);
            //         prev = map.getTileAt(x, y-1);

            //         prev.index = tile.index;

            //         if (y === mapHeight - 1) {
            //             tile.index = Phaser.Math.RND.weightedPick(tiles);
            //         }
            //     }
            // }

            sx = 0;

        }

        this.cameras.main.scrollX = sx;
    }



    useEffect(() => {
        if (!game && containerRef.current) {
            import('phaser').then(({ Game }) => {
                setGameConfig({
                    type: Phaser.AUTO,
                    width: 600,
                    height: 300,
                    scene: {
                        preload: preload,
                        create: create,
                        update: update
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
            <div id="tbContainer" ref={containerRef}></div>
        </div>
    );
}
