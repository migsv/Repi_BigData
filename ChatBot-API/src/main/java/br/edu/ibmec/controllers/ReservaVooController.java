package br.edu.ibmec.controllers;

import br.edu.ibmec.dto.reservavoodto;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.services.reservavooservice;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/reservas-voo")
public class ReservaVooController {

    private final reservavooservice reservaVooService;
    private final UsuarioRepository usuarioRepository;

    public ReservaVooController(reservavooservice reservaVooService, UsuarioRepository usuarioRepository) {
        this.reservaVooService = reservaVooService;
        this.usuarioRepository = usuarioRepository;
    }

    @GetMapping
    public ResponseEntity<List<reservavoodto>> getAllReservas() {
        return ResponseEntity.ok(reservaVooService.obterTodasReservas());
    }

    @GetMapping("/{id}")
    public ResponseEntity<reservavoodto> getReservaById(@PathVariable Long id) {
        Optional<reservavoodto> reserva = reservaVooService.obterReservaPorId(id);
        return reserva.map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<reservavoodto>> getReservasByUsuario(@PathVariable Long usuarioId) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        List<reservavoodto> reservas = reservaVooService.obterPorUsuario(usuario.get());
        return ResponseEntity.ok(reservas);
    }

    @GetMapping("/status/{status}")
    public ResponseEntity<List<reservavoodto>> getReservasByStatus(@PathVariable String status) {
        try {
            var statusEnum = Enum.valueOf(br.edu.ibmec.models.ReservaVoo.StatusReserva.class, status.toUpperCase());
            List<reservavoodto> reservas = reservaVooService.obterPorStatus(statusEnum);
            return ResponseEntity.ok(reservas);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/usuario/{usuarioId}/status/{status}")
    public ResponseEntity<List<reservavoodto>> getReservasByUsuarioAndStatus(@PathVariable Long usuarioId,
                                                                             @PathVariable String status) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        try {
            var statusEnum = Enum.valueOf(br.edu.ibmec.models.ReservaVoo.StatusReserva.class, status.toUpperCase());
            List<reservavoodto> reservas = reservaVooService.obterPorUsuarioEStatus(usuario.get(), statusEnum);
            return ResponseEntity.ok(reservas);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PostMapping
    public ResponseEntity<reservavoodto> createReserva(@RequestBody reservavoodto dto) {
        reservavoodto created = reservaVooService.salvarReserva(dto);
        return ResponseEntity.status(201).body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<reservavoodto> updateReserva(@PathVariable Long id, @RequestBody reservavoodto dto) {
        try {
            reservavoodto updated = reservaVooService.atualizarReserva(id, dto);
            return ResponseEntity.ok(updated);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReserva(@PathVariable Long id) {
        try {
            reservaVooService.deletarReserva(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
