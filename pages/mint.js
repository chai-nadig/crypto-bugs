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

export default function Mint() {

  // FOR WALLET
  const [signedIn, setSignedIn] = useState(false)

  const [walletAddress, setWalletAddress] = useState(null)

  // FOR MINTING
  const [how_many_bugs, set_how_many_bugs] = useState(1)

  const [bugContract, setBugContract] = useState(null)

  // INFO FROM SMART Contract

  const [totalSupply, setTotalSupply] = useState(0)

  const [saleStarted, setSaleStarted] = useState(false)

  const [bugPrice, setBugPrice] = useState(0)

  const [minted, setMinted] = useState(false)

  useEffect(async () => {
    signIn()
  }, [])

  async function signIn() {
    if (typeof window.web3 !== 'undefined') {
      // Use existing gateway
      window.web3 = new Web3(window.ethereum);
    } else {
      alert("No Ethereum interface injected into browser. Read-only access");
    }

//    window.ethereum.enable()
//      .then(function(accounts) {
//        window.web3.eth.net.getNetworkType()
//          // checks if connected network is mainnet (change this to rinkeby if you wanna test on testnet)
//          .then((network) => {
//            console.log(network);
//            if (network != "rinkeby") {
//              alert("You are on " + network + " network. Change network to rinkeby or you won't be able to do anything here")
//            }
//          });
//
//        let wallet = accounts[0]
//        setWalletAddress(wallet)
//        setSignedIn(true)
//        callContractData(wallet)
//
//      })
//      .catch(function(error) {
//        // Handle error. Likely the user rejected the login
//        console.error(error)
//      })

        setSignedIn(false)
  }

  async function signOut() {
    setSignedIn(false)
  }

  async function callContractData(wallet) {
    // let balance = await web3.eth.getBalance(wallet);
    // setWalletBalance(balance)
    const bugContract = new window.web3.eth.Contract(ABI, ADDRESS)
    setBugContract(bugContract)

    const salebool = await bugContract.methods.saleIsActive().call()
    // console.log("saleisActive" , salebool)
    setSaleStarted(salebool)

    const totalSupply = await bugContract.methods.totalSupply().call()
    setTotalSupply(totalSupply)

    const bugPrice = await bugContract.methods.bugPrice().call()
    setBugPrice(bugPrice)
  }

  async function mintBug(how_many_bugs) {
    if (bugContract) {
      const price = Number(bugPrice) * how_many_bugs

      const gasAmount = await bugContract.methods.mintBugs(how_many_bugs).estimateGas({
        from: walletAddress,
        value: price
      })
      console.log("estimated gas", gasAmount)

      console.log({
        from: walletAddress,
        value: price
      })

      bugContract.methods
        .mintBugs(how_many_bugs)
        .send({
          from: walletAddress,
          value: price,
          gas: String(gasAmount)
        })
        .on('transactionHash', function(hash) {
          setMinted(true);
          console.log("transactionHash", hash)
        })
    } else {
      console.log("Wallet not connected")
    }
  };


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
        <div className="flex items-center justify-between absolute top-0 w-full border-b-2 pb-6">
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
      <div className="md:w-2/3 w-4/5">
        <div className="mt-6 border-b-2 py-6">
          <div className="flex flex-col items-center">
            <span className="flex text-5xl text-white items-center my-4 ">TOTAL BUGS MINTED:  <span className="text-red text-6xl"> {!signedIn ?  0 : totalSupply } / 11,111</span></span>
            {saleStarted ?
            <div id="mint" className="flex justify-around  mt-8 mx-6">
              <span className="flex text-5xl text-white items-center bg-grey-lighter rounded rounded-r-none px-3 font-bold">BUG ME</span>
              <input
                type="number"
                min="1"
                max="20"
                value={how_many_bugs}
                onChange={ e => set_how_many_bugs(e.target.value) }
                name=""
                className="pl-4 text-4xl inline bg-grey-lighter  py-2 font-normal rounded text-grey-darkest font-bold" />
              <span className="flex text-5xl text-white items-center bg-grey-lighter rounded rounded-r-none px-3 font-bold">BUGS!</span>
            </div> :<div></div>}
            {saleStarted ?
            <button onClick={() => mintBug(how_many_bugs)} className="mt-4 text-4xl border-6 bg-blau  text-white hover:text-black p-2 ">BUG ME {how_many_bugs} bugs for {(bugPrice * how_many_bugs) / (10 ** 18)} ETH + GAS</button>
            : <button className="mt-4 text-4xl border-6 bg-red  text-white hover:text-black p-2 ">SALE IS NOT ACTIVE</button>
            }

            { minted ? <div className="text-4xl text-crypto-red mt-6 border-b-2 py-6"> Successfully minted {how_many_bugs} bugs! </div>
              : <div></div>
            }
          </div>
        </div>
      </div>
    </div>
  )
}