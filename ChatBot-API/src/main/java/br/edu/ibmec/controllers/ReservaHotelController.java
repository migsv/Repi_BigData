package br.edu.ibmec.controllers;

import br.edu.ibmec.models.ReservaHotel;
import br.edu.ibmec.repository.ReservaHotelRepository;
import br.edu.ibmec.repository.UsuarioRepository;
import lombok.Data;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/reservas-hotel")
public class ReservaHotelController {

    private final ReservaHotelRepository reservaHotelRepository;
    private final UsuarioRepository usuarioRepository;

    public ReservaHotelController(ReservaHotelRepository reservaHotelRepository,
                                  UsuarioRepository usuarioRepository) {
        this.reservaHotelRepository = reservaHotelRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @PostMapping
    public ResponseEntity<ReservaHotel> criarReserva(@RequestBody ReservaHotelRequest request) {
        var usuario = Optional.ofNullable(request.resolveUsuario(usuarioRepository))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "Informe o CPF do usuário."));

        ReservaHotel reserva = new ReservaHotel();
        reserva.setId(UUID.randomUUID().toString());
        reserva.setUsuarioId(usuario.getId());
        reserva.setUsuarioCpf(usuario.getCpf());
        reserva.setNomeHotel(request.getNomeHotel());
        reserva.setLocalizacao(request.getLocalizacao());
        reserva.setDataCheckIn(parseDate(request.getDataCheckIn(), "dataCheckIn"));
        reserva.setDataCheckOut(parseDate(request.getDataCheckOut(), "dataCheckOut"));
        reserva.setPrecoTotal(Optional.ofNullable(request.getPrecoTotal()).orElse(BigDecimal.ZERO));
        reserva.setStatus(resolveStatus(request.getStatus()));

        ReservaHotel saved = reservaHotelRepository.save(reserva);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping
    public ResponseEntity<List<ReservaHotel>> listarTodas() {
        List<ReservaHotel> reservas = new ArrayList<>();
        reservaHotelRepository.findAll().forEach(reservas::add);
        return ResponseEntity.ok(reservas);
    }

    @GetMapping("/cpf/{cpf}")
    public ResponseEntity<List<ReservaHotel>> listarPorCpf(@PathVariable String cpf) {
        return usuarioRepository.findByCpf(cpf)
                .map(usuario -> ResponseEntity.ok(reservaHotelRepository.findByUsuarioId(usuario.getId())))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado."));
    }

    @PatchMapping("/{id}/cancelar")
    public ResponseEntity<ReservaHotel> cancelar(@PathVariable String id) {
        ReservaHotel reserva = reservaHotelRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Reserva não encontrada."));
        reserva.setStatus(ReservaHotel.StatusReserva.CANCELADA);
        ReservaHotel saved = reservaHotelRepository.save(reserva);
        return ResponseEntity.ok(saved);
    }

    private LocalDate parseDate(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            return null;
        }
        try {
            return LocalDate.parse(value);
        } catch (DateTimeParseException e) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Formato inválido para " + fieldName + ". Use ISO-8601 (ex.: 2025-12-15)."
            );
        }
    }

    private ReservaHotel.StatusReserva resolveStatus(String status) {
        if (status == null || status.isBlank()) {
            return ReservaHotel.StatusReserva.CONFIRMADA;
        }
        try {
            return ReservaHotel.StatusReserva.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Status inválido. Use PENDENTE, CONFIRMADA ou CANCELADA."
            );
        }
    }

    @Data
    private static class ReservaHotelRequest {
        private String usuarioCpf;
        private String nomeHotel;
        private String localizacao;
        private String dataCheckIn;
        private String dataCheckOut;
        private BigDecimal precoTotal;
        private String status;

        br.edu.ibmec.models.Usuario resolveUsuario(UsuarioRepository usuarioRepository) {
            if (usuarioCpf == null || usuarioCpf.isBlank()) {
                return null;
            }
            return usuarioRepository.findByCpf(usuarioCpf)
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado para o CPF informado."));
        }
    }
}
