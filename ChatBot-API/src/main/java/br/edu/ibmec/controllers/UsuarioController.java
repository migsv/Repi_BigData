package br.edu.ibmec.controllers;

import br.edu.ibmec.dto.usuariodto;
import br.edu.ibmec.services.usuarioservice;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

    private final usuarioservice usuarioService;

    public UsuarioController(usuarioservice usuarioService) {
        this.usuarioService = usuarioService;
    }

    @GetMapping
    public List<usuariodto> getAllUsers() {
        return usuarioService.obterTodosUsuarios();
    }

    @GetMapping("/{id}")
    public ResponseEntity<usuariodto> getUserById(@PathVariable Long id) {
        Optional<usuariodto> user = usuarioService.obterUsuarioPorId(id);
        return user.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public usuariodto createUser(@RequestBody usuariodto userDTO) {
        return usuarioService.salvarUsuario(userDTO);
    }

    @PutMapping("/{id}")
    public ResponseEntity<usuariodto> updateUser(@PathVariable Long id, @RequestBody usuariodto userDTO) {
        try {
            usuariodto updatedUser = usuarioService.atualizarUsuario(id, userDTO);
            return ResponseEntity.ok(updatedUser);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        usuarioService.deletarUsuario(id);
        return ResponseEntity.noContent().build();
    }
}