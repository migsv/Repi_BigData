package br.edu.ibmec.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.ReservaVooRepository;
import br.edu.ibmec.repository.UsuarioRepository;

@RestController
@RequestMapping("/reservas-voo")
public class ReservaVooController {

    @Autowired
    private ReservaVooRepository reservaVooRepository;
    
    @Autowired
    private UsuarioRepository usuarioRepository;

    @GetMapping
    public ResponseEntity<List<ReservaVoo>> getReservasVoo() {
        return ResponseEntity.ok(reservaVooRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReservaVoo> getReservaVoo(@PathVariable Long id) {
        Optional<ReservaVoo> reserva = reservaVooRepository.findById(id);
        return reserva.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<ReservaVoo>> getReservasByUsuario(@PathVariable Long usuarioId) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        List<ReservaVoo> reservas = reservaVooRepository.findByUsuario(usuario.get());
        return ResponseEntity.ok(reservas);
    }

    @PostMapping
    public ResponseEntity<ReservaVoo> saveReservaVoo(@RequestBody ReservaVoo reservaVoo) {
        ReservaVoo reservaSalva = reservaVooRepository.save(reservaVoo);
        return ResponseEntity.ok(reservaSalva);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ReservaVoo> updateReservaVoo(@PathVariable Long id, @RequestBody ReservaVoo reservaVoo) {
        if (!reservaVooRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaVoo.setId(id);
        ReservaVoo reservaAtualizada = reservaVooRepository.save(reservaVoo);
        return ResponseEntity.ok(reservaAtualizada);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReservaVoo(@PathVariable Long id) {
        if (!reservaVooRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaVooRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}