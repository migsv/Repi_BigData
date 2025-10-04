package br.edu.ibmec.services;
import br.edu.ibmec.dto.reservahoteldto;

public interface reservahotelservice {
    void criarReservaHotel(reservahoteldto reserva);
    reservahoteldto obterReservaHotelPorId(Long id);
    reservahoteldto salvarReservaHotel(reservahoteldto reserva);
    reservahoteldto atualizarReservaHotel(Long id, reservahoteldto reserva);
    void deletarReservaHotel(Long id);
}
