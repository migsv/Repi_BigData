package br.edu.ibmec.services;

import br.edu.ibmec.dto.usuariodto;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UsuarioServiceIMPL implements usuarioservice {

    private final UsuarioRepository usuarioRepository;

    public UsuarioServiceIMPL(UsuarioRepository usuarioRepository) {
        this.usuarioRepository = usuarioRepository;
    }

    @Override
    public List<usuariodto> obterTodosUsuarios() {
        return usuarioRepository.findAll()
                .stream()
                .map(usuario -> new usuariodto(
                        usuario.getId(),
                        usuario.getNome(),
                        usuario.getEmail(),
                        usuario.getTelefone(),
                        usuario.getIdioma(),
                        usuario.getMoeda()
                ))
                .collect(Collectors.toList());
    }

    @Override
    public Optional<usuariodto> obterUsuarioPorId(Long id) {
        return usuarioRepository.findById(id)
                .map(usuario -> new usuariodto(
                        usuario.getId(),
                        usuario.getNome(),
                        usuario.getEmail(),
                        usuario.getTelefone(),
                        usuario.getIdioma(),
                        usuario.getMoeda()
                ));
    }

    @Override
    public usuariodto salvarUsuario(usuariodto usuarioDto) {
        Usuario usuario = new Usuario();
        usuario.setNome(usuarioDto.nome());
        usuario.setEmail(usuarioDto.email());
        usuario.setTelefone(usuarioDto.telefone());
        usuario.setIdioma(usuarioDto.idioma());
        usuario.setMoeda(usuarioDto.moeda());

        Usuario salvo = usuarioRepository.save(usuario);

        return new usuariodto(
                salvo.getId(),
                salvo.getNome(),
                salvo.getEmail(),
                salvo.getTelefone(),
                salvo.getIdioma(),
                salvo.getMoeda()
        );
    }

    @Override
    public usuariodto atualizarUsuario(Long id, usuariodto usuarioDto) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        usuario.setNome(usuarioDto.nome());
        usuario.setEmail(usuarioDto.email());
        usuario.setTelefone(usuarioDto.telefone());
        usuario.setIdioma(usuarioDto.idioma());
        usuario.setMoeda(usuarioDto.moeda());

        Usuario atualizado = usuarioRepository.save(usuario);

        return new usuariodto(
                atualizado.getId(),
                atualizado.getNome(),
                atualizado.getEmail(),
                atualizado.getTelefone(),
                atualizado.getIdioma(),
                atualizado.getMoeda()
        );
    }

    @Override
    public void deletarUsuario(Long id) {
        usuarioRepository.deleteById(id);
    }
}

