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
    var controls;


    function preload() {
        this.load.image("crypto-bugs-world-tiles", "../images/crypto-bugs-world-tiles.png");
        this.load.tilemapCSV("crypto-bugs-world-map", "../assets/crypto-bugs-world-map.csv")
    }

    function create() {
        map = this.make.tilemap({ key: "crypto-bugs-world-map", tileWidth: 24, tileHeight: 24});
        var tileset = map.addTilesetImage("crypto-bugs-world-tiles");
        var layer = map.createLayer(0, tileset, 0, 0);


        // Phaser supports multiple cameras, but you can access the default camera like this:
        const camera = this.cameras.main;

        // Set up the arrows to control the camera
        const cursors = this.input.keyboard.createCursorKeys();
        controls = new Phaser.Cameras.Controls.FixedKeyControl({
            camera: camera,
            left: cursors.left,
            right: cursors.right,
            up: cursors.up,
            down: cursors.down,
            speed: 0.5
        });

        // Constrain the camera so that it isn't allowed to move outside the width/height of tilemap
        camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

    }


    function update(time, delta) {
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
