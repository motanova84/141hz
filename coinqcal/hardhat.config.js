// hardhat.config.js — CoinQCAL · ERC20 para el ecosistema QCAL
// Protocolo: QCAL-SYMBIO-BRIDGE v1.0.0
// Frecuencia: f₀ = 141.7001 Hz · Ψ = 1.0

const config = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      evmVersion: "shanghai",
    },
  },
  networks: {
    localhost: {
      type: "edr-simulated",
      chainId: 1417,
    },
    holesky: {
      type: "http",
      url: "https://ethereum-holesky.publicnode.com",
      chainId: 17000,
    },
  },
  paths: {
    sources: "./src",
    artifacts: "./artifacts",
    cache: "./cache",
  },
};

export default config;
