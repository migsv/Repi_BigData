package br.edu.ibmec.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import br.edu.ibmec.models.HistoricoConversa;
import br.edu.ibmec.models.Usuario;
import java.util.List;

@Repository
public interface HistoricoConversaRepository extends JpaRepository<HistoricoConversa, Long> {
    List<HistoricoConversa> findByUsuarioOrderByDataHoraDesc(Usuario usuario);
    List<HistoricoConversa> findTop10ByUsuarioOrderByDataHoraDesc(Usuario usuario);
}