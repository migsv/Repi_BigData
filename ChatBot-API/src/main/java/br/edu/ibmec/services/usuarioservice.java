package br.edu.ibmec.services;

import br.edu.ibmec.dto.usuariodto;
import java.util.List;
import java.util.Optional;

public interface usuarioservice {
    List<usuariodto> obterTodosUsuarios();
    Optional<usuariodto> obterUsuarioPorId(Long id);
    usuariodto salvarUsuario(usuariodto usuario);
    usuariodto atualizarUsuario(Long id, usuariodto usuario);
    void deletarUsuario(Long id);
}
