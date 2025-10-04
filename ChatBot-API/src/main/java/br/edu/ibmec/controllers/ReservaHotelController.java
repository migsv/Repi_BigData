package br.edu.ibmec.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.edu.ibmec.models.ReservaHotel;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.ReservaHotelRepository;
import br.edu.ibmec.repository.UsuarioRepository;

@RestController
@RequestMapping("/reservas-hotel")
public class ReservaHotelController {

    @Autowired
    private ReservaHotelRepository reservaHotelRepository;
    
    @Autowired
    private UsuarioRepository usuarioRepository;

    @GetMapping
    public ResponseEntity<List<ReservaHotel>> getReservasHotel() {
        return ResponseEntity.ok(reservaHotelRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReservaHotel> getReservaHotel(@PathVariable Long id) {
        Optional<ReservaHotel> reserva = reservaHotelRepository.findById(id);
        return reserva.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<ReservaHotel>> getReservasByUsuario(@PathVariable Long usuarioId) {
        Optional<Usuario> usuario = usuarioRepository.findById(usuarioId);
        if (usuario.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        List<ReservaHotel> reservas = reservaHotelRepository.findByUsuario(usuario.get());
        return ResponseEntity.ok(reservas);
    }

    @PostMapping
    public ResponseEntity<ReservaHotel> saveReservaHotel(@RequestBody ReservaHotel reservaHotel) {
        ReservaHotel reservaSalva = reservaHotelRepository.save(reservaHotel);
        return ResponseEntity.ok(reservaSalva);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ReservaHotel> updateReservaHotel(@PathVariable Long id, @RequestBody ReservaHotel reservaHotel) {
        if (!reservaHotelRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaHotel.setId(id);
        ReservaHotel reservaAtualizada = reservaHotelRepository.save(reservaHotel);
        return ResponseEntity.ok(reservaAtualizada);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReservaHotel(@PathVariable Long id) {
        if (!reservaHotelRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        reservaHotelRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}