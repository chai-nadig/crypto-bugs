import Head from 'next/head'
export default function Home() {
return (
<div id="bodyy" className="flex flex-col items-center justify-center min-h-screen py-2">
  <Head>
    <title>crypto-bugs</title>
    <link rel="icon" href="/images/favicon.png" />
    <meta property="og:title" content="crypto-bugs" key="ogtitle" />
    <meta property="og:description" content="bugs in production. we ship them" key="ogdesc" />
    <meta property="og:type" content="website" key="ogtype" />
    <meta property="og:url" content="https://crypto-bugs.com/" key="ogurl"/>
    <meta property="og:image" content="https://crypto-bugs.com/images/13.png" key="ogimage"/>
    <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
    <meta name="twitter:card" content="summary_large_image" key="twcard"/>
    <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
    <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
    <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
    <meta name="twitter:description" content="bugs in production. we ship them" key="twdesc" />
    <meta name="twitter:image" content="https://crypto-bugs.com/images/13.png" key="twimage" />
  </Head>
  <div>
    <div className="flex items-center justify-between w-full border-b-2	pb-6">
      <div className="border-4 border-red-800 p-1">
        <a href="/" className=""><img src="images/13.png" width="120px" className="logo-image" /></a>
      </div>

      <nav className="flex flex-wrap flex-row justify-around">
        <a href="/#about" className="text-4xl text-white-shadow hover:text-black m-6">About</a>
        <a href="/#severity" className="text-4xl text-white-shadow hover:text-black m-6">Severity</a>
        <a href="/#traits" className="text-4xl text-white-shadow hover:text-black m-6">Traits</a>
        <a href="/#roadmap" className="text-4xl text-white-shadow hover:text-black m-6">Roadmap</a>
        <a href="/mint" className="text-4xl text-white-shadow hover:text-black m-6">Mint</a>
        <a href="/#team" className="text-4xl text-white-shadow hover:text-black m-6">Team</a>
      </nav>
    </div>
  </div>
  <div className="md:w-2/3 w-4/5 " id="about">
    <div className="mt-6 border-b-2 py-6">
      <h1 className="text-6xl text-center text-white"><span className="text-crypto-red">crypto-bugs-0x2b67</span></h1>
      <div className="flex flex-wrap lg:flex-nowrap justify-around items-center py-6">
        <div className="lg:w-1/2 w-3/4">
          <p className="text-2xl text-white my-6">We've discovered a variety of bugs and triaged their severities.

          </p>
          <p className="text-2xl text-white my-6">
            On <span className="text-red">11/11/21</span> a detailed bug report of <span className="text-red">11,111</span> (0x2b67 in hexadecimal) bugs will be released. <br/>
          </p>
          <p className="text-2xl text-white my-6">
            First 111 swatters who bring along three friends to the bug bash will receive an NFT of the bug for free!<br/>
          </p>
          <p>
            <span class="text-red text-2xl">Join our Discord <u><a className="text-white-shadow hover:text-black" target="_blank" href="https://discord.gg/Sw2PgseN">here!</a></u></span>
          </p>
        </div>
        <div className="border-4 border-red-500 p-2">
          <img  src="images/1391.png" width="240px" />
        </div>
      </div>
    </div>
    <div id="severity" className="justify-around items-center mx-6 py-6 border-b-2">
      <h2 className="text-crypto-red text-6xl text-center">SEVERITY</h2>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="border-4 border-red-500 p-2">
          <img src="images/ani2.gif" alt="" width="240px" class="feature-image"/>
        </div>
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <p class="text-2xl text-white my-6">
            Severity levels more or less correspond to the rarity of traits.
            <ul>
              <li> <span className="text-red-700">blocker </span></li>
              <li> <span className="text-red-600">critical </span> </li>
              <li> <span className="text-red-500">major </span> </li>
              <li> <span className="text-red-400">minor </span> </li>
              <li> <span className="text-red-300">trivial </span> </li>
            </ul>
          </p>
        </div>
      </div>
    </div>
    <div id="traits" className="mx-6 py-6 border-b-2">
      <h2 className="text-crypto-red text-6xl text-center">TRAITS</h2>
      <p class="text-2xl text-white my-6"><b>crypto-bugs-0x2b67</b> have traits like background, accessory, color, spots, and eye color.
        There are some bugs with combinations of unique backgrounds and accessories.
      </p>
      <div className="flex flex-wrap  items-center mx-6 py-6">
        <div className="md:w-1/2">
          <div className=" p-2"><span class="text-white">sunset bug</span><img src="images/set2/1216.png" alt="" width="400" className="feature-image"/>
          </div>
        </div>
        <div className="md:w-1/2 flex flex-wrap">
          <div className=" p-2 "><span class="text-white">hipster bug</span><img src="images/set2/1815.png" alt="" width="200px" className="feature-image"/></div>
          <div className=" p-2 "><span class="text-white">angel bug</span><img src="images/set2/1265.png" alt="" width="200px" className="feature-image"/></div>
          <div className=" p-2 "><span class="text-white">witch bug</span><img src="images/set2/1479.png" alt="" width="200px" className="feature-image"/></div>
          <div className=" p-2 "><span class="text-white">grad bug</span><img src="images/set2/1646.png" alt="" width="200px" className="feature-image"/></div>
        </div>
      </div>
      <p class="text-xl text-white my-6"><i>name your bug as you please!</i>
      </p>

    </div>
    <div id="roadmap" className="mx-6 py-6 border-b-2">
      <h2 className="text-crypto-red text-6xl text-center">ROADMAP</h2>
      <div className="flex flex-wrap justify-around items-center mx-6 py-6">
        <div className="border-4 border-red-500 p-2">
          <img src="images/set3/3.png"  width="240px" class="feature-image"/>
        </div>
        <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
          <span className="text-red text-4xl">LAUNCH - 11/11/21</span>
          <p class="text-2xl text-white my-6">
            <span className="text-red">Start of our bug bash!</span><br/>
             Reporting 11,111 bugs.
            First 111 swatters who bring along three friends will receive an NFT of the bug for free!
          </p>
           <p>
            <span class="text-red text-2xl">Join our Discord <u><a className="text-white-shadow hover:text-black" target="_blank" href="https://discord.gg/Sw2PgseN">here!</a></u></span>
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
    <div id="team" className="mx-12 my-16 ">
      <h2 className="text-crypto-red text-6xl text-center">TEAM</h2>
      <div className="flex justify-around flex-wrap">
        <div className="flex flex-col  my-6">
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
          <h3 className="my-4 text-center text-5xl text-center text-red hover:text-red">uv</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-3xl">Community Manager</span><br/>
            uv@crypto-bugs.com
          </p>
        </div>
        <div className="flex flex-col  my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
        </div>
      </div>
      <p class="text-2xl text-white my-6">
        We're three software techies, that got really engrossed in the world of NFT recently. Mostly inspired by
        <a className="text-white-shadow hover:text-black" href="https://www.theverge.com/2021/3/11/22325054/beeple-christies-nft-sale-cost-everydays-69-million" target="_blank"> Beeple's sale for $69 Million</a>
        &nbsp; and <a className="text-white-shadow hover:text-black" href="https://www.larvalabs.com/cryptopunks" target="_blank"> 24 x 24 bit art by Cryptopunks,</a>
        &nbsp; we came up with <b className="text-red ">crypto-bugs-0x2b67.</b>
      </p>
      <p class="text-2xl text-white my-6">
        <b className="text-red ">crypto-bugs-0x2b67 </b> took two weeks to go from idea to product.
        We bought a drawing tablet one weekend, started drawing bugs, adding backgrounds and accessories, and that was a lot of fun!
        It's amazing how much you can do in a 24 x 24 pixel canvas!
      </p>
      <p className="text-center">
         <span class="text-red text-3xl">Join our Discord <u><a className="text-white-shadow hover:text-black" target="_blank" href="https://discord.gg/Sw2PgseN">here!</a></u></span>
      </p>
    </div>
  </div>
</div>
)
}