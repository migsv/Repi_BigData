package br.edu.ibmec.services;

import br.edu.ibmec.dto.reservavoodto;
import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.models.Usuario;

import java.util.List;
import java.util.Optional;

public interface reservavooservice {
    List<reservavoodto> obterTodasReservas();
    Optional<reservavoodto> obterReservaPorId(Long id);
    reservavoodto salvarReserva(reservavoodto reserva);
    reservavoodto atualizarReserva(Long id, reservavoodto reserva);
    void deletarReserva(Long id);
    
    List<reservavoodto> obterPorUsuario(Usuario usuario);
    List<reservavoodto> obterPorStatus(ReservaVoo.StatusReserva status);
    List<reservavoodto> obterPorUsuarioEStatus(Usuario usuario, ReservaVoo.StatusReserva status);
}

