package br.edu.ibmec.repository;

import br.edu.ibmec.models.ReservaVoo;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReservaVooRepository extends CosmosRepository<ReservaVoo, String> {
    List<ReservaVoo> findByUsuarioId(String usuarioId);
}
