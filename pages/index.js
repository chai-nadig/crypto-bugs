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
    <meta property="og:image" content="https://crypto-bugs.com/images/bug.png" key="ogimage"/>
    <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
    <meta name="twitter:card" content="summary_large_image" key="twcard"/>
    <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
    <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
    <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
    <meta name="twitter:description" content="bugs in production. we ship them" key="twdesc" />
    <meta name="twitter:image" content="https://crypto-bugs.com/images/bug.png" key="twimage" />
  </Head>
  <div>
    <div className="flex items-center justify-between w-full border-b-2	pb-6">
      <div className="border-4 border-red-800 p-1">
        <a href="/" className=""><img src="images/13.png" width="120px" className="logo-image" /></a>
      </div>

      <nav className="flex flex-wrap flex-row justify-around">
        <a href="/#about" className="text-4xl text-white hover:text-black m-6">About</a>
        <a href="/#severity" className="text-4xl text-white hover:text-black m-6">Severity</a>
        <a href="/#traits" className="text-4xl text-white hover:text-black m-6">Traits</a>
        <a href="/#roadmap" className="text-4xl text-white hover:text-black m-6">Roadmap</a>
        <a href="/mint" className="text-4xl text-white hover:text-black m-6">Mint</a>
        <a href="/#team" className="text-4xl text-white hover:text-black m-6">Team</a>
      </nav>
    </div>
  </div>
  <div className="md:w-2/3 w-4/5 " id="about">
    <div className="mt-6 border-b-2 py-6">
      <div className="flex flex-wrap lg:flex-nowrap justify-around items-center">
        <div className="lg:w-1/2 w-3/4">
          <h1 className="text-6xl text-white"><span className="text-crypto-red">crypto-bugs-0x2b67</span></h1>
          <p className="text-2xl text-white my-6">We've discovered a variety of bugs and triaged then under different severities.
            A detailed <span class="text-bold-underlined">bug report</span> will be released soon.
          </p>
          <p className="text-2xl text-white my-6">
            On 11/11 we will be reporting 11,111 (0x2b67 in hexadecimal) bugs. <br/>
          </p>
          <p className="text-2xl text-white my-6">
            <b>The first 111 swatters who join our bug bash will receive an NFT of the bug for free!</b><br/>
            <span class="text-red">Join our Discord <u><a target="_blank" href="https://discord.gg/Sw2PgseN">here!</a></u></span>
          </p>
          <p className="text-2xl text-white my-6">
            <strong>RELEASE:</strong> 11/11/2021. 1:00 pm PST.<br />
            <span className="text-white text-2xl"><strong>TOTAL SUPPLY: 11,111</strong> bugs.<br/>
            <strong>PRICE: 0.025 ETH </strong>each.</span>
          </p>
          <iframe src="https://free.timeanddate.com/countdown/i7vcex5b/n107/cf11/cm0/cu4/ct0/cs1/ca2/co0/cr0/ss0/cacfff/cpcfff/pct/tcfff/fn3/fs100/szw448/szh189/iso2021-11-11T21:00:00" allowtransparency="true" frameBorder="0" width="425" height="25"></iframe>
        </div>
        <div className="border-4 border-red-500 p-2">
          <img  src="images/1391.png" width="240px" />
        </div>
      </div>
    </div>
    <div id="severity" className="flex flex-wrap justify-around items-center mx-6 py-6 border-b-2">
      <div className="border-4 border-red-500 p-2">
        <img src="images/ani2.gif" alt="" width="240px" class="feature-image"/>
      </div>
      <div className="flex flex-col justify-between mx-6 sm:w-1/2 w-4/5 py-6 ">
        <h2 className="text-crypto-red text-6xl text-center">SEVERITY</h2>
        <p class="text-2xl text-white my-6">
          Severity levels more or less correspond to the rarity of traits.
        <ul>
          <li> blocker </li>
          <li> critical </li>
          <li> major </li>
          <li> minor </li>
          <li> trivial </li>
        </ul>
        </p>
      </div>
    </div>
    <div id="traits" className="mx-6 py-6 border-b-2">
      <h2 className="text-crypto-red text-6xl text-center">TRAITS</h2>
      <p class="text-2xl text-white my-6"><b>crypto-bugs-0x2b67</b> have traits like background, accessory, color, spots and eye color.
        There are some bugs with combinations of a unique background and an accessory.
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
      <h2 className="text-6xl text-center text-crypto-red my-4">ROADMAP</h2>

      <p className="text-xl text-white my-6  montserrat">Ever since the inception of the <span className="text-5xl Poppitandfinch ">boring</span> <span className="text-blau text-5xl Poppitandfinchsans">Bugs</span> <span className="text-5xl Poppitandfinch">company</span> after <a target="_blank" href="https://twitter.com/thedigitalvee/status/1405896585142280192" className="underline text-black font-bold">this tweet</a>, our goal has been to <span className="text-blau text-5xl Poppitandfinchsans">GIVE BACK</span> as much as possible.
      </p>
      <p className="text-xl text-white my-6 montserrat"> A minimum of
        <span className="font-bold"> 25% of all sales</span> are donated to charity.
      </p>
      <p className="text-xl text-white my-6  montserrat"> At 100% sellout, we pledge to donate <span className="font-bold"> 60 ETH </span> from primary sales.
      </p>
      <h2 className="text-6xl text-center text-crypto-red my-4">HOW WE'RE GIVING BACK</h2>
      <ul className="">
        <li className="text-xl text-white my-6  montserrat"><span className="font-bold"> 4 x 10 ETH donations: </span> The first of these will be made to <a target="_blank" href="https://girlswhocode.com/" className="underline text-black font-bold">Girls Who Code</a>, working to empower young women and <span className="font-bold"> close the gender gap </span> in technology. We know women are unrepresented in the NFT space - lets help to fix this! The remaining donations will be made via community vote using <a target="_blank" href="https://thegivingblock.com/" className="underline text-black font-bold">the Giving Block</a>.</li>
        <li className="text-xl text-white my-6  montserrat"><span className="font-bold"> 20 ETH to Community Wallet: </span> Directed towards supporting creators that want to make a positive contribution to the NFT space.</li>
        <li className="text-xl text-white my-6  montserrat"><span className="font-bold"> Secondary sales: 5% royalty </span> (2.5% donation, 2.5% to the team). Secondary sales are directed towards charities voted on by the community monthly.</li>
      </ul>
      <p className="text-xl text-white my-6 montserrat"> In addition, we have been, and continue to make <span className="font-bold underline"> high quality content for the NFT community </span> through our <span className="font-bold underline"> PROJECT IN PROGRESS </span> series, to help budding creators to along their journey.
      </p>
      <p className="text-xl text-white my-6 montserrat"> All fully annotated source code for image generation and the smart contract will be made available after launch as a community resource.
      </p>
    </div>
    <div id="team" className="mx-12 my-16 ">
      <h2 className="text-crypto-red text-6xl text-center">TEAM</h2>
      <div className="flex justify-around flex-wrap">
        <div className="flex flex-col  my-6" style={{width:"360px"}}>
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-5xl text-center text-red">hellstealz</h3>
          <a href="mailto:hellstealz@crypto-bugs.com" className="text-center text-4xl text-center underline text-white"> hellstealz@crypto-bugs.com</a>
        </div>
        <div className="flex flex-col  my-6" style={{width:"360px"}}>
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-5xl text-center text-red">ag</h3>
          <a href="mailto:ag@crypto-bugs.com" className="text-center text-4xl text-center underline text-white"> ag@crypto-bugs.com </a>
        </div>
      </div>
      <div className="flex justify-around flex-wrap">
        <div className="flex flex-col  my-6" style={{width:"360px"}}>
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image"/></div>
          <h3 className="my-4 text-center text-4xl text-center text-red"><u><a target="_blank" href="https://discord.gg/Sw2PgseN">Join our discord</a></u></h3>
        </div>
      </div>
    </div>
  </div>
</div>
)
}