package br.edu.ibmec.services;
import br.edu.ibmec.dto.reservahoteldto;

import java.util.List;
import java.util.Optional;

public interface reservahotelservice {
    List<reservahoteldto> obterTodasReservas();
    Optional<reservahoteldto> obterReservaPorId(Long id);
    reservahoteldto salvarReserva(reservahoteldto reserva);
    reservahoteldto atualizarReserva(Long id, reservahoteldto reserva);
    void deletarReserva(Long id);
}
