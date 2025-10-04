package br.edu.ibmec.services;

import br.edu.ibmec.dto.usuariodto;

public interface usuarioservice {

    void criarUsuario(usuariodto usuario);
    usuariodto obterUsuarioPorId(Long id);
    usuariodto salvarUsuario(usuariodto usuario);
    void atualizarUsuario(Long id, usuariodto usuario);
    void deletarUsuario(Long id);
}
