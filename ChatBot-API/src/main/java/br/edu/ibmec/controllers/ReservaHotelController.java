package br.edu.ibmec.controllers;

import br.edu.ibmec.dto.reservahoteldto;
import br.edu.ibmec.services.reservahotelservice;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/reservas-hotel")
public class ReservaHotelController {

    @Autowired
    private reservahotelservice reservaHotelService;


    @GetMapping
    public ResponseEntity<List<reservahoteldto>> getReservasHotel() {
        return ResponseEntity.ok(reservaHotelService.obterTodasReservas());
    }

    @GetMapping("/{id}")
    public ResponseEntity<reservahoteldto> getReservaHotel(@PathVariable Long id) {
        Optional<reservahoteldto> reserva = reservaHotelService.obterReservaPorId(id);
        return reserva.map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<reservahoteldto> saveReservaHotel(@RequestBody reservahoteldto reserva) {
        reservahoteldto salva = reservaHotelService.salvarReserva(reserva);
        return ResponseEntity.ok(salva);
    }

    @PutMapping("/{id}")
    public ResponseEntity<reservahoteldto> updateReservaHotel(@PathVariable Long id, @RequestBody reservahoteldto reserva) {
        reservahoteldto atualizada = reservaHotelService.atualizarReserva(id, reserva);
        return ResponseEntity.ok(atualizada);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteReservaHotel(@PathVariable Long id) {
        reservaHotelService.deletarReserva(id);
        return ResponseEntity.noContent().build();
    }
}
