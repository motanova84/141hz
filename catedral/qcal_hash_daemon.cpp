#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <cstring>
#include <sstream>
#include <iomanip>
#include <functional>

const double F_0 = 141.7001;
const double PSI_OBJETIVO = 0.999999;
const int PRIMO_ESTRUCTURAL = 7;

struct ShareQCAL {
    std::string block_header;
    uint64_t nonce;
    std::string worker;
    bool fase_armonica;
    double coherencia;
};

bool verificar_fase_adelica(const std::string& block_header_hex, uint64_t nonce) {
    size_t hash_val = std::hash<std::string>{}(block_header_hex) + nonce;
    return (hash_val % PRIMO_ESTRUCTURAL == 0);
}

double calcular_coherencia(double hashrate_mhs, double latencia_ms) {
    double I = hashrate_mhs;
    double A_eff = 1.0 - std::min(1.0, std::abs(latencia_ms - 0.343) / 10.0);
    return I * (A_eff * A_eff);
}

std::string sellar_qcal(const std::string& worker, uint64_t nonce, bool aceptado) {
    std::ostringstream sello;
    sello << "QCAL|f0=" << F_0
          << "|nonce=" << nonce
          << "|worker=" << worker
          << "|aceptado=" << (aceptado ? "1" : "0")
          << "|psi=" << PSI_OBJETIVO;
    return sello.str();
}

int main(int argc, char* argv[]) {
    std::cout << "[QCAL-C++] Stradivarius Hash Daemon v1.0" << std::endl;
    std::cout << "[QCAL-C++] f0 = " << F_0 << " Hz | Psi >= " << PSI_OBJETIVO << std::endl;
    std::cout << "[QCAL-C++] Primo estructural: " << PRIMO_ESTRUCTURAL << std::endl;
    std::cout << "[QCAL-C++] Modo: ";

    if (argc < 3) {
        std::cout << "DAEMON" << std::endl;
        std::cout << "[QCAL-C++] Escuchando... (usar: qcal_hash_daemon <block_header> <nonce>)" << std::endl;
        return 0;
    }

    std::string block_header = argv[1];
    uint64_t nonce = std::stoull(argv[2]);
    std::string worker = (argc > 3) ? argv[3] : "noesis88.001";

    std::cout << "TEST" << std::endl;
    std::cout << "[QCAL-C++] Header: " << block_header.substr(0, 20) << "..." << std::endl;
    std::cout << "[QCAL-C++] Nonce: " << nonce << std::endl;

    bool fase = verificar_fase_adelica(block_header, nonce);
    std::string sello = sellar_qcal(worker, nonce, fase);

    if (fase) {
        std::cout << "[QCAL-C++] RESULTADO: FASE_ARMONICA | " << sello << std::endl;
        return 0;
    } else {
        std::cout << "[QCAL-C++] RESULTADO: VACIO_ACTIVO | Share descartado | " << sello << std::endl;
        return 1;
    }
}
