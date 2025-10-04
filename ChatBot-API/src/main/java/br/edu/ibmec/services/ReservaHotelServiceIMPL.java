package br.edu.ibmec.services;

import br.edu.ibmec.dto.reservahoteldto;
import br.edu.ibmec.dto.usuariodto;
import br.edu.ibmec.models.ReservaHotel;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.ReservaHotelRepository;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ReservaHotelServiceIMPL implements reservahotelservice {

    private final ReservaHotelRepository reservaHotelRepository;
    private final UsuarioRepository usuarioRepository;
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public ReservaHotelServiceIMPL(ReservaHotelRepository reservaHotelRepository,
                                   UsuarioRepository usuarioRepository) {
        this.reservaHotelRepository = reservaHotelRepository;
        this.usuarioRepository = usuarioRepository;
    }

    private reservahoteldto toDto(ReservaHotel reserva) {
        usuariodto usuarioDto = new usuariodto(
                reserva.getUsuario().getId(),
                reserva.getUsuario().getNome(),
                reserva.getUsuario().getEmail(),
                reserva.getUsuario().getTelefone(),
                reserva.getUsuario().getIdioma(),
                reserva.getUsuario().getMoeda()
        );

        return new reservahoteldto(
            reserva.getId(),
            usuarioDto,
            reserva.getNomeHotel(),
            reserva.getCodigoApiHotel(),
            reserva.getLocalizacao(),
            reserva.getDataCheckIn() != null ? reserva.getDataCheckIn().format(DATE_FORMATTER) : null,
            reserva.getDataCheckOut() != null ? reserva.getDataCheckOut().format(DATE_FORMATTER) : null,
            reserva.getPrecoTotal() != null ? reserva.getPrecoTotal().toString() : null,
            reserva.getStatus() != null ? reserva.getStatus().name() : null,
            reserva.getDataCriacao() != null ? reserva.getDataCriacao().toString() : null
        );
    }

    @Override
    public List<reservahoteldto> obterTodasReservas() {
        return reservaHotelRepository.findAll().stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<reservahoteldto> obterReservaPorId(Long id) {
        return reservaHotelRepository.findById(id)
                .map(this::toDto);
    }

    @Override
    public reservahoteldto salvarReserva(reservahoteldto dto) {
        Usuario usuario = usuarioRepository.findById(dto.usuario().id())
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        ReservaHotel reserva = new ReservaHotel();
        reserva.setUsuario(usuario);
        reserva.setNomeHotel(dto.nomeHotel());
        reserva.setCodigoApiHotel(dto.codigoApiHotel());
        reserva.setDataCheckIn(dto.dataCheckIn() != null ? LocalDate.parse(dto.dataCheckIn(), DATE_FORMATTER) : null);
        reserva.setDataCheckOut(dto.dataCheckOut() != null ? LocalDate.parse(dto.dataCheckOut(), DATE_FORMATTER) : null);
        reserva.setPrecoTotal(dto.precoTotal() != null ? new BigDecimal(dto.precoTotal()) : null);

        ReservaHotel salvo = reservaHotelRepository.save(reserva);
        return toDto(salvo);
    }

    @Override
    public reservahoteldto atualizarReserva(Long id, reservahoteldto dto) {
        ReservaHotel reserva = reservaHotelRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reserva não encontrada"));

        Usuario usuario = usuarioRepository.findById(dto.usuario().id())
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        reserva.setUsuario(usuario);
        reserva.setNomeHotel(dto.nomeHotel());
        reserva.setCodigoApiHotel(dto.codigoApiHotel());
        reserva.setDataCheckIn(dto.dataCheckIn() != null ? LocalDate.parse(dto.dataCheckIn(), DATE_FORMATTER) : null);
        reserva.setDataCheckOut(dto.dataCheckOut() != null ? LocalDate.parse(dto.dataCheckOut(), DATE_FORMATTER) : null);
        reserva.setPrecoTotal(dto.precoTotal() != null ? new BigDecimal(dto.precoTotal()) : null);

        ReservaHotel atualizado = reservaHotelRepository.save(reserva);
        return toDto(atualizado);
    }

    @Override
    public void deletarReserva(Long id) {
        reservaHotelRepository.deleteById(id);
    }
}


