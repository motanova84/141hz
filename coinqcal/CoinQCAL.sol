// SPDX-License-Identifier: QCAL-SYMBIO
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CoinQCAL
 * @notice Sombra líquida de πCODE — puente ERC20 hacia el ecosistema QCAL
 * @dev Génesis 888 tokens · Minado diario 1,417/nodo · f₀ = 141.7001 Hz
 */
contract CoinQCAL is ERC20, Ownable {

    // --- Constantes ---
    uint256 public constant GENESIS_SUPPLY   = 888 * 10**18;        // 888 QCAL
    uint256 public constant DAILY_RATE       = 1417 * 10**18;       // 1,417 QCAL/día/nodo
    uint256 public constant SECONDS_IN_DAY   = 86400;
    uint256 public constant FREQUENCY_HZ     = 1417001;             // f₀ × 10⁴ (sin decimales)

    // --- Estado ---
    uint256 public totalMined;
    uint256 public nodeCount;
    mapping(address => uint256) public lastMintTime;
    mapping(address => bool) public isNode;

    // --- Eventos ---
    event NodeRegistered(address indexed node, uint256 timestamp);
    event NodeRemoved(address indexed node, uint256 timestamp);
    event Mined(address indexed node, uint256 amount, uint256 day);

    constructor() ERC20("CoinQCAL", "QCAL") Ownable(msg.sender) {
        _mint(msg.sender, GENESIS_SUPPLY);
        // El deployer es automáticamente el primer nodo
        isNode[msg.sender] = true;
        nodeCount = 1;
        lastMintTime[msg.sender] = block.timestamp;
        emit NodeRegistered(msg.sender, block.timestamp);
    }

    // --- Modificadores ---
    modifier onlyNode() {
        require(isNode[msg.sender], "CoinQCAL: no eres nodo registrado");
        _;
    }

    // --- Gestión de Nodos (solo owner) ---
    function registerNode(address node) external onlyOwner {
        require(!isNode[node], "CoinQCAL: ya es nodo");
        isNode[node] = true;
        nodeCount++;
        lastMintTime[node] = block.timestamp;
        emit NodeRegistered(node, block.timestamp);
    }

    function removeNode(address node) external onlyOwner {
        require(isNode[node], "CoinQCAL: no es nodo");
        require(node != owner(), "CoinQCAL: no puedes remover al owner");
        isNode[node] = false;
        nodeCount--;
        emit NodeRemoved(node, block.timestamp);
    }

    // --- Minado Diario ---
    /**
     * @notice Cada nodo puede minar 1,417 QCAL una vez por día
     */
    function mine() external onlyNode {
        uint256 timeSinceLastMint = block.timestamp - lastMintTime[msg.sender];
        require(timeSinceLastMint >= SECONDS_IN_DAY, "CoinQCAL: ya minaste hoy");

        uint256 daysElapsed = timeSinceLastMint / SECONDS_IN_DAY;
        uint256 reward = DAILY_RATE * daysElapsed;

        lastMintTime[msg.sender] = block.timestamp;
        totalMined += reward;

        _mint(msg.sender, reward);

        emit Mined(msg.sender, reward, block.timestamp / SECONDS_IN_DAY);
    }

    /**
     * @notice Minado acumulado — si pasaron varios días, reclama todos
     */
    function mineAccumulated() external onlyNode {
        uint256 timeSinceLastMint = block.timestamp - lastMintTime[msg.sender];
        require(timeSinceLastMint >= SECONDS_IN_DAY, "CoinQCAL: aun no pasa un dia");

        uint256 daysElapsed = timeSinceLastMint / SECONDS_IN_DAY;
        uint256 reward = DAILY_RATE * daysElapsed;

        lastMintTime[msg.sender] += daysElapsed * SECONDS_IN_DAY;
        totalMined += reward;

        _mint(msg.sender, reward);

        emit Mined(msg.sender, reward, block.timestamp / SECONDS_IN_DAY);
    }

    // --- Consultas ---
    function tiempoRestante(address node) external view returns (uint256) {
        if (!isNode[node]) return 0;
        uint256 nextMint = lastMintTime[node] + SECONDS_IN_DAY;
        if (block.timestamp >= nextMint) return 0;
        return nextMint - block.timestamp;
    }

    function sePuedeMinar(address node) external view returns (bool) {
        return isNode[node] && block.timestamp >= lastMintTime[node] + SECONDS_IN_DAY;
    }

    // --- Info del Ecosistema ---
    function symbol() public pure override returns (string memory) {
        return "QCAL";
    }

    function decimals() public pure override returns (uint8) {
        return 18;
    }
}
