import Head from 'next/head'
export default function Home() {

  let image1 = "images/set2/1216.png";
  let imageDesc1 = "sunset bug";

  let image2 = "images/set2/1815.png";
  let imageDesc2 = "hipster bug";

  let image3 = "images/set2/1265.png";
  let imageDesc3 = "angel bug";

  let image4 = "images/set2/1479.png";
  let imageDesc4 = "witch bug";

  let image5 = "images/set2/1646.png";
  let imageDesc5 = "grad bug";

return (
<div id="bodyy" className="flex flex-col items-center justify-center min-h-screen py-2">
  <Head>
    <title>crypto-bugs</title>
    <link rel="icon" href="/images/favicon.png" />
    <meta property="og:title" content="crypto-bugs" key="ogtitle" />
    <meta property="og:description" content="a variety of NFT bugs triaged under severities blocker, critical, major, minor and trivial" key="ogdesc" />
    <meta property="og:type" content="website" key="ogtype" />
    <meta property="og:url" content="https://crypto-bugs.com/" key="ogurl"/>
    <meta property="og:image" content="https://crypto-bugs.com/images/13.png" key="ogimage"/>
    <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
    <meta name="twitter:card" content="summary_large_image" key="twcard"/>
    <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
    <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
    <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
    <meta name="twitter:description" content="a variety of NFT bugs triaged under severities blocker, critical, major, minor and trivial." key="twdesc" />
    <meta name="twitter:image" content="https://crypto-bugs.com/images/13.png" key="twimage" />
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu+Mono" />
  </Head>

  <div className="md:w-2/3 w-4/5" >
    <div id="about" className="mx-6 py-8">
      <div className="mt-6 py-1">
        <h1 className="text-6xl text-center text-crypto-red">crypto-bugs-0x2b67</h1>
        <p className="text-2xl text-center text-white my-6"><span className="text-red">11,111</span> (<span className="text-red">0x2b67</span> in hexadecimal) unique lady bugs.</p>
      </div>

      <div className="mt-6" >
        <div className="items-center">
          <nav className="flex flex-wrap flex-row justify-center">
            <a href="https://twitter.com/CryptoBugsx2B67" target="_blank"><img src="images/twitter.png" width="50px"/></a>
            <a href="https://discord.gg/A6nkdvr2yR" target="_blank"><img src="images/discord.png" width="50px"/></a>
          </nav>
        </div>
      </div>
    </div>
    

    <div id="traits" className="mx-6 py-8">
      <h4 className="text-crypto-red text-6xl text-center py-10">TRAITS</h4>
      <div className="flex flex-wrap justify-center mx-6 py-10">
        <div className="md:w-1/2">
          <div>
            <span class="text-white text-lg">{imageDesc1}</span>
            <img src={image1}  className="feature-image w-4/5"/>
          </div>
        </div>
        <div className="md:w-1/2">
          <div className="flex flex-wrap justify-center">
            <div className=" md:w-1/2 p-1">
              <span class="text-white text-lg">{imageDesc2}</span>
              <img src={image2} className="feature-image w-4/5"/>
            </div>
            <div className="md:w-1/2  p-1">
              <span class="text-white text-lg">{imageDesc3}</span>
              <img src={image3} className="feature-image w-4/5"/>
            </div>
            <div className="md:w-1/2  p-1">
              <span class="text-white text-lg">{imageDesc4}</span>
              <img src={image4} className="feature-image w-4/5"/>
            </div>
            <div className="md:w-1/2  p-1">
              <span class="text-white text-lg">{imageDesc5}</span>
              <img src={image5} className="feature-image w-4/5"/>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    
    <div id="roadmap" className="mx-6 py-8">
      <h2 className="text-crypto-red text-6xl text-center py-10">ROADMAP</h2>
      <div className="flex flex-wrap justify-around items-center mx-6 py-10">
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/3.png"  width="240px" class="feature-image"/>
        </div>
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-4xl">Launch</span>
          <p class="text-2xl text-white my-6">
            <span className="text-red">Start of our bug bash!</span><br/>
             Reporting 11,111 bugs.
            First 111 swatters who bring along three friends will receive an NFT of the bug for free!
          </p>
           <p>
            <span class="text-red text-2xl">Join our Discord <u><a className="text-white-shadow hover:text-black" target="_blank" href="https://discord.gg/A6nkdvr2yR">here!</a></u></span>
          </p>
        </div>
      </div>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-right text-4xl">11% SOLD</span>
          <p class="text-2xl text-right text-white my-6">
            <span className="text-red">Free T-Shirts!</span><br/>
            Swatters with bugs that have <b>exclusive traits</b> will be eligible for a free T-Shirt printed with their bug!
          </p>
          <p class="text-2xl text-right text-white my-6">
          Trait will be revealed after 11% of bugs are sold. Claim your T-Shirt on our website.
          </p>
        </div>
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/2.png"  width="240px" class="feature-image"/>
        </div>
      </div>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/5.png"  width="240px" class="feature-image"/>
        </div>
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-4xl">33% SOLD</span>
          <p class="text-2xl text-white my-6">
            <span className="text-red">Donate to <u><a className="text-white-shadow hover:text-black" href="https://www.catf.us/" target="_blank">Clean Air Task Force</a></u></span><br/>
            We are concerned about the climate! This is how we want to give back.
          </p>
          <p class="text-2xl text-white my-6">
            We will donate 10.18 ETH (11.11% of sales) after 3,666 bugs have sold.
          </p>
        </div>
      </div>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-right text-4xl">66% SOLD</span>
          <p class="text-2xl text-right text-white my-6">
            <span className="text-red">Twitter Banners!</span><br/>
            All swatters will get a Twitter Banner to show off your cool bugs! Claim your banner on our website.
          </p>
        </div>
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/1.jpeg"  width="240px" class="feature-image"/>
        </div>
      </div>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/4.png"  width="240px" class="feature-image"/>
        </div>
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-4xl">99% SOLD</span>
          <p class="text-2xl text-white my-6">
            <span className="text-red">Another round of donation</span><br/>
            This time we'll donate to two non-profits that are chosen by the community.
          </p>
          <p class="text-2xl text-white my-6">
            In this round, we will totally donate 29.41 ETH (11.11% of remaining sales) after 10,999 bugs have sold.
          </p>
        </div>
      </div>
    </div>
    
    
    <div id="team" className="mx-12 my-16 border-b-2 py-8">
      <h2 className="text-crypto-red text-6xl text-center py-10">TEAM</h2>
      <div className="flex justify-around flex-wrap py-10">
        <div className="flex flex-col my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">hellstealz</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Artist | Engineer</span><br/>
            hellstealz@crypto-bugs.com
          </p>
        </div>
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-5xl text-center text-red">ag</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Engineer</span><br/>
            ag@crypto-bugs.com
          </p>
        </div>
      </div>
      <div className="flex justify-around flex-wrap">
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">theladybug</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Comms</span><br/>
            theladybug@crypto-bugs.com
          </p>
        </div>
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
        </div>
      </div>
      <p className="text-center py-8">
         <span class="text-red text-3xl">Join our Discord <u><a className="text-white-shadow hover:text-black" target="_blank" href="https://discord.gg/A6nkdvr2yR">here!</a></u></span>
      </p>
    </div>
    <div id="verified-contract" className="mx-12 my-16 border-b-2 py-6">
      <h2 className="text-crypto-red text-6xl text-center">VERIFIED CONTRACT</h2>
      <div className="flex justify-around flex-wrap">
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-3xl text-center text-white-shadow hover:text-black">
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