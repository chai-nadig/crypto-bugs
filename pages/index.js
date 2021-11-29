import Head from 'next/head'
import {
  useState,
  useEffect
} from 'react';
export default function Home() {

  const [traits, setTraits] = useState([]);

  const [showTraits, setShowTraits] = useState(false);

  const allTraits = [
    ["sunset bug", "images/set2/1216.png"],
    ["hipster bug", "images/set2/1815.png"],
    ["angel bug", "images/set2/473.png"],
    ["witch bug", "images/set2/1479.png"],
    ["grad bug","images/set2/1383.png" ],
    ["beach bug", "images/set2/1396.png"],
    ["queen bug", "images/set2/138.png"],
    ["road bug", "images/set2/1420.png"],
    ["love bug", "images/set2/3432.png"],
    ["snow bug", "images/set2/387.png"],
    ["island bug", "images/set2/512.png"],
    ["hard hat bug", "images/set2/1837.png"],
    ["book bug", "images/set2/3710.png"],
    ["matrix bug", "images/set2/330.png"],
    ["tux bug", "images/set2/6.png"],
    ["chef bug", "images/set2/212.png"],
    ["desert bug", "images/set2/458.png"],
    ["clown bug", "images/set2/1646.png"],
    ["viking bug", "images/set2/1671.png"],
    ["turban bug", "images/set2/1832.png"],
    ["beanie bug", "images/set2/1913.png"],
    ["sunglasses bug", "images/set2/1969.png"],
  ];

  useEffect(async () => {
    setTraits(shuffle(allTraits))
    setShowTraits(true);
  }, [])
  

  function shuffle (array) {
    let currentIndex = array.length,  randomIndex;
  
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



return (
<div id="bodyy" className="flex flex-col items-center justify-center min-h-screen py-2">
  <Head>
    <title>crypto-bugs</title>
    <link rel="icon" href="/images/3811.png" />
    <meta property="og:title" content="crypto-bugs" key="ogtitle" />
    <meta property="og:description" content="a loveliness of 11,111 ladybugs" key="ogdesc" />
    <meta property="og:type" content="website" key="ogtype" />
    <meta property="og:url" content="https://crypto-bugs.com/" key="ogurl"/>
    <meta property="og:image" content="https://crypto-bugs.com/images/3811.png" key="ogimage"/>
    <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
    <meta name="twitter:card" content="summary_large_image" key="twcard"/>
    <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
    <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
    <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
    <meta name="twitter:description" content="a loveliness of 11,111 ladybugs" key="twdesc" />
    <meta name="twitter:image" content="https://crypto-bugs.com/images/3811.png" key="twimage" />
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu+Mono" />
  </Head>

  <div className="md:w-2/3 w-4/5" >
    <div id="about" className="py-10">
      <div className="py-10">
        <h1 className="text-5xl mg:text-6xl lg:text-6xl text-center text-crypto-red">crypto-bugs</h1>
        <p className="text-2xl text-center text-white my-6">
          A <span className="italic">loveliness</span> of <span className="text-red">11,111</span> ladybugs.
        </p>
      </div>

      <div className="py-10">
        <div className="items-center">
          <nav className="flex flex-wrap flex-row justify-center">
            <a href="https://twitter.com/CryptoBugsx2B67" target="_blank"><img src="images/twitter.png" width="50px"/></a>
            <a href="https://discord.gg/A6nkdvr2yR" target="_blank"><img src="images/discord.png" width="50px"/></a>
          </nav>
        </div>
      </div>
    </div>
    
    {showTraits ? 
    <div id="traits" className="py-10">
      <h2 className="text-crypto-red text-5xl text-center">TRAITS</h2>
      <div className="flex flex-wrap px-4 py-10">
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5  grid justify-items-center">
          <span class="text-white text-lg">{traits[0][0]}</span>
          <img src={traits[0][1]} className="w-11/12 rounded-lg"/>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5 grid justify-items-center">
          <span class="text-white text-lg">{traits[1][0]}</span>
          <img src={traits[1][1]} className="w-11/12 rounded-lg"/>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5  grid justify-items-center">
          <span class="text-white text-lg">{traits[2][0]}</span>
          <img src={traits[2][1]} className="w-11/12 rounded-lg"/>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5  grid justify-items-center">
          <span class="text-white text-lg">{traits[3][0]}</span>
          <img src={traits[3][1]} className="w-11/12 rounded-lg"/>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5  grid justify-items-center">
          <span class="text-white text-lg">{traits[4][0]}</span>
          <img src={traits[4][1]} className="w-11/12 rounded-lg"/>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 py-3 px-5  grid justify-items-center">
          <span class="text-white text-lg">{traits[5][0]}</span>
          <img src={traits[5][1]} className="w-11/12 rounded-lg"/>
        </div>
      </div>
    </div>
    : <div></div> }
    
    
    <div id="lifecycle" className="py-10">
      <h2 className="text-crypto-red text-6xl text-center">LIFECYCLE</h2>
      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/3.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">0%</span> Eggs</span>
          <p class="text-xl text-white">
             The eggs are laid. The loveliness is yet to hatch. We're running a giveaway where the first 111 ladybugs will be adopted for free.
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/2.png" className="w-11/12 rounded-lg"/>
        </div>

        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pl-10 lg:pl-10 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">11%</span> Larva</span>
          <p class="text-xl text-white">
            The loveliness has hatched. Once 11% of the ladybugs are adopted, we will choose a trait and all ladybugs with the 
            chosen trait will be printed on T-Shirts.
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/5.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">33%</span> Pupa</span>
          <p class="text-xl text-white">
             The ladybugs have started showing colors at this stage. To ensure they have a healthy environment to grow,  
             we will donate 10.18 ETH (11.11% of sales) to <a className="text-red hover:text-white" href="https://www.catf.us/" target="_blank">Clean Air Task Force.</a> 
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 pb-6">
          <img src="images/set3/1.jpeg"  className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pl-10 lg:pl-10 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">66%</span> Young Adults</span>
          <p class="text-xl text-white">
             Our ladybugs have grown into a loveliness of young adults, and they deserve to be celebrated. 
             We will make banners for every ladybug, so you can show off your ladybugs on Twitter.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/4.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">99%</span> Adults</span>
          <p class="text-xl text-white">
             A loveliness of fully grown adult ladybugs. This time we'll donate to two non-profits that are chosen by the community.
             A total of 29.41 ETH (11.11% of remaining sales) will be donated.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/6.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">100%</span> Flown</span>
          <p class="text-xl text-white">
             All ladybugs have spread their wings and flown. What happens next? We're happy to let you all decide. 
             Until you speard your wings, you have no idea how far you can fly... :)
          </p>
        </div>
      </div>        
    </div>

    <div id="team" className="py-10">
      <h2 className="text-crypto-red text-6xl text-center">TEAM</h2>
      <div className="flex flex-wrap items-center py-8">
        <div className="w-full grid place-items-center md:w-1/3 lg:w-1/3  py-10">
          <div>
            <img src="images/set4/hellstealz.png" className="w-11/12 rounded-full h-24 w-24"/>
          </div>
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">
            <a href="https://twitter.com/hellstealzz" target="_blank">hellstealz</a>
          </h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Artist | Engineer</span><br/>
              hellstealz@crypto-bugs.com
          </p>
        </div>
        <div className="w-full grid place-items-center md:w-1/3 lg:w-1/3  py-10">
          <div>
            <img src="images/set4/ag.png" className="w-11/12 rounded-full h-24 w-24"/>
          </div>
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">
            <a href="https://twitter.com/Agmahi" target="_blank">ag</a>
          </h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Engineer</span><br/>
              ag@crypto-bugs.com
          </p>
        </div>
        <div className="w-full grid place-items-center md:w-1/3 lg:w-1/3 py-10">
          <div>
            <img src="images/set4/theladybug.png" className="w-11/12 rounded-full h-24 w-24"/>
          </div>
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">
            <a href="https://twitter.com/UshaVellala" target="_blank">theladybug</a>
          </h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Comms</span><br/>
              theladybug@crypto-bugs.com
          </p>
        </div>
      </div>
    </div>
    
    <div id="verified-contract" className="py-10">
      <h2 className="text-crypto-red text-6xl text-center">VERIFIED CONTRACT</h2>
      <div className="flex flex-wrap justify-around py-10">
        <div className="flex flex-col my-6">
          <h3 className="my-4 text-3xl text-center text-white hover:text-red">
            <a href="https://etherscan.io/address/0x83e9b2ef39e28ecb3c6b0e8a72488f22dc668bde" target="_blank">View on Ethereum</a>
          </h3>
        </div>
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-3xl text-center text-white">Verified and Published</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-2xl text-red">11/11/2021 10:23:38 AM +UTC</span><br/>
          </p>
        </div>
      </div>
    </div>
  </div>
</div>
)
}