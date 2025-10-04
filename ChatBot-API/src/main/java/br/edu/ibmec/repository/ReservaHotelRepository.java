package br.edu.ibmec.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import br.edu.ibmec.models.ReservaHotel;
import br.edu.ibmec.models.Usuario;
import java.util.List;

@Repository
public interface ReservaHotelRepository extends JpaRepository<ReservaHotel, Long> {
    List<ReservaHotel> findByUsuario(Usuario usuario);
    List<ReservaHotel> findByStatus(ReservaHotel.StatusReserva status);
    List<ReservaHotel> findByUsuarioAndStatus(Usuario usuario, ReservaHotel.StatusReserva status);
}