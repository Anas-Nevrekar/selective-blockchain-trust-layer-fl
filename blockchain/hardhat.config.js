require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24",
  networks: {
    ganache: {
      url: "http://127.0.0.1:7545",
      accounts: ["0x4f1ba1da7fc2e56ffce6f0d7a92465efde9bf76d13c6321bb2a548eff6bfc46d"]
    }
  }
};
