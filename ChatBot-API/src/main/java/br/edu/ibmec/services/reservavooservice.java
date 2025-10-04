package br.edu.ibmec.services;
import br.edu.ibmec.dto.reservavoodto;

public interface reservavooservice {

  void criarReservaVoo(reservavoodto reserva);
  reservavoodto obterReservaVooPorId(Long id);
  reservavoodto salvarReservaVoo(reservavoodto reserva);
  reservavoodto atualizarReservaVoo(Long id, reservavoodto reserva);
  void deletarReservaVoo(Long id);
}
