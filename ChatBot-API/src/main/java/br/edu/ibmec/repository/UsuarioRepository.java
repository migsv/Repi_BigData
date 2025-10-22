package br.edu.ibmec.repository;

import org.springframework.stereotype.Repository;
import br.edu.ibmec.models.Usuario;
import java.util.Optional;

import com.azure.spring.data.cosmos.repository.CosmosRepository;

@Repository
public interface UsuarioRepository extends CosmosRepository<Usuario, String> {
    Optional<Usuario> findByCpf(String cpf);
}