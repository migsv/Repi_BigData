package br.edu.ibmec.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.models.Usuario;
import java.util.List;

@Repository
public interface ReservaVooRepository extends JpaRepository<ReservaVoo, Long> {
    List<ReservaVoo> findByUsuario(Usuario usuario);
    List<ReservaVoo> findByStatus(ReservaVoo.StatusReserva status);
    List<ReservaVoo> findByUsuarioAndStatus(Usuario usuario, ReservaVoo.StatusReserva status);
}