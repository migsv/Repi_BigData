package br.edu.ibmec.controllers;

import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.repository.ReservaVooRepository;
import br.edu.ibmec.repository.UsuarioRepository;
import lombok.Data;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/reservas-voo")
public class ReservaVooController {

    private final ReservaVooRepository reservaVooRepository;
    private final UsuarioRepository usuarioRepository;

    public ReservaVooController(ReservaVooRepository reservaVooRepository, UsuarioRepository usuarioRepository) {
        this.reservaVooRepository = reservaVooRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @PostMapping
    public ResponseEntity<ReservaVoo> criarReserva(@RequestBody ReservaVooRequest request) {
        String usuarioId = Optional.ofNullable(request.resolveUsuarioId())
                .map(String::trim)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "O campo usuario.id é obrigatório."));

        if (usuarioRepository.findById(usuarioId).isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado.");
        }

        ReservaVoo reserva = new ReservaVoo();
        reserva.setId(UUID.randomUUID().toString());
        reserva.setUsuarioId(usuarioId);
        reserva.setCompanhiaAerea(request.getCompanhiaAerea());
        reserva.setOrigem(request.getOrigem());
        reserva.setDestino(request.getDestino());
        reserva.setDataPartida(parseDate(request.getDataPartida(), "dataPartida"));
        reserva.setDataRetorno(parseDate(request.getDataRetorno(), "dataRetorno"));
        reserva.setPreco(Optional.ofNullable(request.getPreco()).orElse(BigDecimal.ZERO));
        reserva.setStatus(resolveStatus(request.getStatus()));

        ReservaVoo saved = reservaVooRepository.save(reserva);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<ReservaVoo>> listarPorUsuario(@PathVariable String usuarioId) {
        List<ReservaVoo> reservas = reservaVooRepository.findByUsuarioId(usuarioId);
        return ResponseEntity.ok(reservas);
    }

    private LocalDateTime parseDate(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            return null;
        }
        try {
            return LocalDateTime.parse(value);
        } catch (DateTimeParseException e) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Formato inválido para " + fieldName + ". Use ISO-8601 (ex.: 2025-12-15T09:30:00)."
            );
        }
    }

    private ReservaVoo.StatusReserva resolveStatus(String status) {
        if (status == null || status.isBlank()) {
            return ReservaVoo.StatusReserva.PENDENTE;
        }
        try {
            return ReservaVoo.StatusReserva.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Status inválido. Use PENDENTE, CONFIRMADA ou CANCELADA."
            );
        }
    }

    @Data
    private static class ReservaVooRequest {
        private UsuarioRef usuario;
        private String usuarioId;
        private String origem;
        private String destino;
        private String dataPartida;
        private String dataRetorno;
        private BigDecimal preco;
        private String companhiaAerea;
        private String status;

        String resolveUsuarioId() {
            if (usuarioId != null && !usuarioId.isBlank()) {
                return usuarioId;
            }
            if (usuario != null && usuario.getId() != null && !usuario.getId().isBlank()) {
                return usuario.getId();
            }
            return null;
        }

        @Data
        private static class UsuarioRef {
            private String id;
        }
    }
}
