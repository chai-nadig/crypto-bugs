import Head from 'next/head'
import Web3 from "web3";
import {
  useState,
  useEffect
} from 'react';
import {
  ADDRESS,
  ABI
} from "../config.js"
import MetaMaskOnboarding from '@metamask/onboarding'

export default function Home() {

  // METAMASK
  const [isMetamaskInstalled, setIsMetamaskInstalled] = useState(false);

  // FOR WALLET
  const [isMetamaskConnected, setIsMetamaskConnected] = useState(false);

  const [metamaskButtonText, setMetamaskButtonText] = useState('');

  const [walletAddress, setWalletAddress] = useState(null);

  // FOR MINTING
  const [numberOfBugsText, setNumberOfBugsText] = useState('');

  const [minted, setMinted] = useState(0)

  const [transactionLink, setTransactionLink] = useState('')

  const [bugContract, setBugContract] = useState(null);

  // INFO FROM SMART Contract

  const [totalSupply, setTotalSupply] = useState(0);

  const [saleStarted, setSaleStarted] = useState(false);

  const [bugPrice, setBugPrice] = useState(0);

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
    setTraits(shuffle(allTraits));
    setShowTraits(true);
    checkMetamaskInstalled();
  }, [])

  function updateNumberOfBugs(n) {
    let b = parseInt(n);
    if (b > 20) {
      setNumberOfBugsText('20');
    }
    else if (b < 0) {
      setNumberOfBugsText('0');
    }
    else {
      setNumberOfBugsText(n);
    }
  }

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

  //Created check function to see if the MetaMask extension is installed
  const checkMetamaskInstalled = () => {
    //Have to check the ethereum binding on the window object to see if it's installed
    const { ethereum } = window;
    let installed = Boolean(ethereum && ethereum.isMetaMask);
    setIsMetamaskInstalled(installed);
    if (!installed) {
      setMetamaskButtonText('INSTALL METAMASK');
    } else {
      if (isMetamaskConnected) {
        console.log('metamask is connected')
      } else {
        setMetamaskButtonText('CONNECT METAMASK');
      }
    }
  }


  //This will start the onboarding proccess
  async function installMetamask() {
    //We create a new MetaMask onboarding object to use in our app
    const onboarding = new MetaMaskOnboarding();

    //On this object we have startOnboarding which will start the onboarding process for our end user
    onboarding.startOnboarding();
  }

  function onClickMetamask() {
    console.log('onClickMetamask');
    if (isMetamaskInstalled) {
      console.log('metamask is installed');
      if (isMetamaskConnected) {
        console.log('metamask is connected');
      } else {
        console.log('going to signin');
        connectMetamask();
      }
    } else {
      installMetamask();
    }
  }

  async function connectMetamask() {
    if (typeof window.web3 !== 'undefined') {
      // Use existing gateway
      window.web3 = new Web3(window.ethereum);
    } else {
      alert("No Ethereum interface injected into browser. Read-only access");
    }

    ethereum.enable()
      .then(function(accounts){


        let wallet = accounts[0]
        setWalletAddress(wallet)
        setIsMetamaskConnected(true)
        callContractData(wallet)
        console.log(wallet);
    });
  }

  async function callContractData(wallet) {
    const bugContract = new window.web3.eth.Contract(ABI, ADDRESS);
    setBugContract(bugContract);

    const salebool = await bugContract.methods.saleIsActive().call();
    setSaleStarted(salebool);

    const totalSupply = await bugContract.methods.totalSupply().call()
    setTotalSupply(totalSupply);

    const bugPrice = await bugContract.methods.bugPrice().call()
    setBugPrice(bugPrice);
  }

  async function mintBug(n) {
    if (bugContract) {
      const price = Number(bugPrice) * n
      const gasAmount = await bugContract.methods.mintBugs(n).estimateGas({
        from: walletAddress,
        value: price
      })

      bugContract.methods
        .mintBugs(n)
        .send({
          from: walletAddress,
          value: price,
          gas: String(gasAmount)
        })
        .on('transactionHash', function(hash) {
          setMinted(n);
          setNumberOfBugsText('')

          window.web3.eth.net.getNetworkType()
            .then((network) => {
              if (network == 'mainnet') {
                setTransactionLink('https://etherscan.io/tx/' + hash)
              } else {
                setTransactionLink('https://' + network + '.etherscan.io/tx/' + hash)
              }
            })
        })
    }
  };

return (
<div id="bodyy" className="flex flex-col items-center justify-center min-h-screen py-2">
  <Head>
    <title>crypto-bugs</title>
    <link rel="icon" href="/images/3811.png" />
    <meta property="og:title" content="crypto-bugs" key="ogtitle" />
    <meta property="og:description" content="An NFT loveliness of 11,111 ladybugs" key="ogdesc" />
    <meta property="og:type" content="website" key="ogtype" />
    <meta property="og:url" content="https://crypto-bugs.com/" key="ogurl"/>
    <meta property="og:image" content="https://crypto-bugs.com/images/3811.png" key="ogimage"/>
    <meta property="og:site_name" content="https://crypto-bugs.com/" key="ogsitename" />
    <meta name="twitter:card" content="summary_large_image" key="twcard"/>
    <meta property="twitter:domain" content="crypto-bugs.com" key="twdomain" />
    <meta property="twitter:url" content="https://crypto-bugs.com/" key="twurl" />
    <meta name="twitter:title" content="crypto-bugs" key="twtitle" />
    <meta name="twitter:description" content="An NFT loveliness of 11,111 ladybugs" key="twdesc" />
    <meta name="twitter:image" content="https://crypto-bugs.com/images/3811.png" key="twimage" />
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu+Mono" />
  </Head>

  <div className="w-4/5 md:w-2/3 lg:w-2/3">
    <div id="about" className="py-10">
      <div className="py-10">
        <h1 className="text-5xl text-center text-crypto-red">crypto-bugs</h1>
        <p className="text-2xl text-center text-white my-6">
          An NFT <span className="italic">loveliness</span> of <span className="text-red">11,111</span> ladybugs.
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
      <div className="flex flex-wrap">
        <div className="w-full md:w-2/3 lg:w-2/3 grid justify-items-center">
          <div className="flex flex-wrap">
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[0][0]}</span>
              <img src={traits[0][1]} className="w-11/12 rounded-lg"/>
            </div>
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[1][0]}</span>
              <img src={traits[1][1]} className="w-11/12 rounded-lg"/>
            </div>
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[2][0]}</span>
              <img src={traits[2][1]} className="w-11/12 rounded-lg"/>
            </div>
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[3][0]}</span>
              <img src={traits[3][1]} className="w-11/12 rounded-lg"/>
            </div>
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[4][0]}</span>
              <img src={traits[4][1]} className="w-11/12 rounded-lg"/>
            </div>
            <div className="w-full md:w-1/3 lg:w-1/3 py-3 grid justify-items-center">
              <span className="text-white text-lg">{traits[5][0]}</span>
              <img src={traits[5][1]} className="w-11/12 rounded-lg"/>
            </div>
          </div>
        </div>
        <div className="w-full md-w-1/3 lg:w-1/3 grid justify-items-center">
          <div className="w-full flex flex-wrap">
          <div className="w-full grid justify-items-center pt-10 pb-3">
            <div className="w-11/12 flex flex-wrap py-3 border border-red-500 rounded-lg grid justify-items-center">
              <div className="w-full px-3 py-3">
                <p className="text-white text-2xl text-center ">MINTED {totalSupply.toLocaleString('en-US')} / 11,111</p>
                <p className="text-crypto-red text-xl text-center ">
                  {saleStarted ? <span>&nbsp;</span> : <span>Sale is not active</span> }
                </p>
              </div>
              <div className="w-full h-full px-3 py-3 grid justify-items-center">
                <img src={traits[6][1]} className="w-55 py-1 rounded-lg"/>
              </div>
              <div className="w-full px-3 grid justify-items-center">
                <div className="w-full flex flex-wrap">
                  { isMetamaskConnected ?
                  <div className="w-full flex flex-wrap px-5">
                    <div className="w-1/2">
                      <span className="text-white text-xl">Quantity</span>
                      <input type="number" value={numberOfBugsText} onChange={e => updateNumberOfBugs(e.target.value)}
                      placeholder="MAX 20"
                      className="w-4/5 px-3 text-xl md:text-2xl lg:text-2xl inline py-2 rounded text-black" />
                    </div>
                    <div className="w-1/2">
                      <span className="text-white text-xl">Price</span>
                      <input
                        type="text" value={JSON.stringify((bugPrice * (numberOfBugsText != '' ? parseInt(numberOfBugsText) : 0)) / (10 ** 18)) + ' ETH'} disabled={true}
                        className="w-full px-3 text-xl md:text-2xl bg-white lg:text-2xl inline py-2 rounded text-black" />
                    </div>
                    <div className="w-full pt-3">
                      <button className={`w-full text-white text-2xl disabled:opacity-40 bg-red-700 py-2 rounded-sm ${saleStarted && parseInt(numberOfBugsText) > 0? 'hover:bg-red-600' : ''}`}
                        onClick={() => mintBug(parseInt(numberOfBugsText))} disabled={!saleStarted || !(parseInt(numberOfBugsText) > 0)}> MINT
                      </button>
                    </div>
                    <div className="w-full pt-1">
                      <p className="text-crypto-red hover:text-red-600 text-lg text-center">
                        { minted > 0 ? <a href={ transactionLink } target="_blank" className="underline">View transaction</a> : <span>&nbsp;</span> }
                      </p>
                    </div>
                  </div>
                   :
                  <div className="w-full flex flex-wrap">
                    <div className="w-full py-3 px-5">
                      <button className="w-full text-white text-2xl py-2 rounded-sm bg-metamask hover:bg-metamask-hover" onClick={ onClickMetamask }>
                        { metamaskButtonText }
                      </button>
                    </div>
                  </div>
                  }
                </div>
              </div>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>
    : <div></div> }
    
    
    <div id="lifecycle" className="py-10">
      <h2 className="text-crypto-red text-5xl text-center">LIFECYCLE</h2>
      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/1.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">0%</span> Eggs</span>
          <p className="text-xl text-white">
             The eggs are laid, a loveliness is yet to hatch. We're running a giveaway where the first 100 ladybugs will be adopted for free.
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/2.png" className="w-11/12 rounded-lg"/>
        </div>

        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pl-20 lg:pl-20 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">11%</span> Larva</span>
          <p className="text-xl text-white">
            The smallest among us are the bravest of all, the loveliness has hatched! Once 11% of the ladybugs are adopted, we will choose a trait and all ladybugs with the 
            chosen trait will be printed on T-Shirts.
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/3.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">33%</span> Pupa</span>
          <p className="text-xl text-white">
            Growing in all places they ever can, to ensure our loveliness has a clean world to live in,  
            we will donate 10.18 ETH to <a className="text-red hover:text-white" href="https://www.catf.us/" target="_blank">Clean Air Task Force.</a> 
          </p>
        </div>
      </div>
      
      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/4.png"  className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pl-20 lg:pl-20 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">66%</span> Young Adults</span>
          <p className="text-xl text-white">
            Our ladybugs are now a loveliness of young adults, living young and wild and free.
            We will make banners for every ladybug, so you can show off your ladybugs on Twitter.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center py-8">
        <div className="w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/5.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pr-20 lg:pr-20 text-justify">
          <span className="text-4xl text-white text-center md:text-left lg:text-left py-3"><span className="text-red ">99%</span> Adults</span>
          <p className="text-xl text-white">
             Splattering specks of red and black, a loveliness of fully grown adult ladybugs. 
             We will donate to two non-profits chosen by the community.
             A total of 29.41 ETH will be donated.
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center py-8">
        <div className="md:order-last lg:order-last w-full place-items-center md:w-1/3 lg:w-1/3 grid md:px-20 lg:px-20 px-10 py-10">
          <img src="images/set3/6.png" className="w-11/12 rounded-lg"/>
        </div>
        <div className="flex flex-col md:w-2/3 lg:w-2/3 md:pl-20 lg:pl-20 text-justify">
          <span className="text-4xl text-white text-center md:text-right lg:text-right py-3"><span className="text-red ">100%</span> Flown</span>
          <p className="text-xl text-white">
             All ladybugs have spread their wings and flown. What happens next? We're happy to let you all decide. 
             Until you speard your wings, you have no idea how far you can fly...
          </p>
        </div>
      </div>        
    </div>

    <div id="team" className="py-10">
      <h2 className="text-crypto-red text-5xl text-center">TEAM</h2>
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
      <h2 className="text-crypto-red text-5xl text-center">VERIFIED CONTRACT</h2>
      <div className="flex flex-wrap justify-around py-10">
        <div className="flex flex-col my-6">
          <div className="cards-image-mask"><img src="" width="360px" alt="" className="cards-image" /></div>
          <h3 className="my-4 text-center text-3xl text-center text-white">Published</h3>
          <p className="text-center text-white text-2xl">
            <span className="text-2xl text-red">11/11/2021 10:23:38 AM +UTC</span><br/>
          </p>
        </div>
        <div className="flex flex-col my-6">
          <h3 className="my-4 text-3xl text-center text-white hover:text-red-300">
            <a href="https://etherscan.io/address/0x83e9b2ef39e28ecb3c6b0e8a72488f22dc668bde" target="_blank">View on Ethereum</a>
          </h3>
        </div>
      </div>
    </div>

    <div id="footer" className="py-10">
      <div className="flex flex-wrap">
        <div className="w-full md:w-1/3 lg:w-1/3">
          <p className="text-gray-300 text-lg text-center">© 2021 Crypto Bugs</p>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3 text-white text-lg">
          <div className="flex flex-wrap flex-row justify-center">
            <a href="https://twitter.com/CryptoBugsx2B67" target="_blank"><img src="images/twitter.png" width="40px"/></a>
            <a href="https://discord.gg/A6nkdvr2yR" target="_blank"><img src="images/discord.png" width="40px"/></a>
          </div>
        </div>
        <div className="w-full md:w-1/3 lg:w-1/3">
          <p className="text-gray-300 text-lg text-center hover:text-red-300 underline">
            <a href="/terms-conditions">Terms & Conditions</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</div>
)
}