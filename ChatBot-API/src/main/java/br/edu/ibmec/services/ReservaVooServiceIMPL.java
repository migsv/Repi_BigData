package br.edu.ibmec.services;

import br.edu.ibmec.dto.reservavoodto;
import br.edu.ibmec.dto.usuariodto;
import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.ReservaVooRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ReservaVooServiceIMPL implements reservavooservice {

    private final ReservaVooRepository reservaVooRepository;

    public ReservaVooServiceIMPL(ReservaVooRepository reservaVooRepository) {
        this.reservaVooRepository = reservaVooRepository;
    }


    private reservavoodto toDto(ReservaVoo reserva) {
        usuariodto usuarioDto = new usuariodto(
                reserva.getUsuario().getId(),
                reserva.getUsuario().getNome(),
                reserva.getUsuario().getEmail(),
                reserva.getUsuario().getTelefone(),
                reserva.getUsuario().getIdioma(),
                reserva.getUsuario().getMoeda()
        );

        return new reservavoodto(
            reserva.getId(),
            usuarioDto,
            reserva.getCompanhiaAerea(),
            reserva.getOrigem(),
            reserva.getDestino(),
            reserva.getDataPartida(),
            reserva.getDataRetorno(),
            reserva.getPreco(),
            reserva.getStatus().name()
        );
    }

    @Override
    public List<reservavoodto> obterTodasReservas() {
        return reservaVooRepository.findAll().stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<reservavoodto> obterReservaPorId(Long id) {
        return reservaVooRepository.findById(id).map(this::toDto);
    }

   @Override
        public reservavoodto salvarReserva(reservavoodto reserva) {
            ReservaVoo novaReserva = new ReservaVoo();
            Usuario usuario = new Usuario();
            usuario.setId(reserva.usuario().id());
            novaReserva.setUsuario(usuario);
            novaReserva.setOrigem(reserva.origem());
            novaReserva.setDestino(reserva.destino());
            novaReserva.setDataPartida(reserva.dataPartida());
            novaReserva.setDataRetorno(reserva.dataRetorno());
            novaReserva.setCompanhiaAerea(reserva.companhiaAerea());
            novaReserva.setPreco(reserva.preco());
            novaReserva.setStatus(ReservaVoo.StatusReserva.valueOf(reserva.status()));

            ReservaVoo salvo = reservaVooRepository.save(novaReserva);
            return toDto(salvo);
        }


    @Override
    public reservavoodto atualizarReserva(Long id, reservavoodto reservavoodto) {
        ReservaVoo reserva = reservaVooRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reserva não encontrada"));

        reserva.setOrigem(reservavoodto.origem());
        reserva.setDestino(reservavoodto.destino());
        reserva.setDataPartida(reservavoodto.dataPartida());
        reserva.setDataRetorno(reservavoodto.dataRetorno());
        reserva.setCompanhiaAerea(reservavoodto.companhiaAerea());
        reserva.setPreco(reservavoodto.preco());
        reserva.setStatus(reservavoodto.status() != null 
        ? ReservaVoo.StatusReserva.valueOf(reservavoodto.status()) 
        : ReservaVoo.StatusReserva.PENDENTE);

        ReservaVoo atualizado = reservaVooRepository.save(reserva);
        return toDto(atualizado);
    }

    @Override
    public void deletarReserva(Long id) {
        reservaVooRepository.deleteById(id);
    }

    @Override
    public List<reservavoodto> obterPorUsuario(Usuario usuario) {
        return reservaVooRepository.findByUsuario(usuario)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Override
    public List<reservavoodto> obterPorStatus(ReservaVoo.StatusReserva status) {
        return reservaVooRepository.findByStatus(status)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Override
    public List<reservavoodto> obterPorUsuarioEStatus(Usuario usuario, ReservaVoo.StatusReserva status) {
        return reservaVooRepository.findByUsuarioAndStatus(usuario, status)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }
}
