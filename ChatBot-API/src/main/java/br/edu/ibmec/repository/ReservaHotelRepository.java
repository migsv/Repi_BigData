package br.edu.ibmec.repository;

import br.edu.ibmec.models.ReservaHotel;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReservaHotelRepository extends CosmosRepository<ReservaHotel, String> {
    List<ReservaHotel> findByUsuarioId(String usuarioId);
}
