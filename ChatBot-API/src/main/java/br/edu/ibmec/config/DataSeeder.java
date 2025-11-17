package br.edu.ibmec.config;

import br.edu.ibmec.models.ReservaHotel;
import br.edu.ibmec.models.ReservaVoo;
import br.edu.ibmec.models.Usuario;
import br.edu.ibmec.repository.ReservaHotelRepository;
import br.edu.ibmec.repository.ReservaVooRepository;
import br.edu.ibmec.repository.UsuarioRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Component
public class DataSeeder implements CommandLineRunner {

    private final UsuarioRepository usuarioRepository;
    private final ReservaVooRepository reservaVooRepository;
    private final ReservaHotelRepository reservaHotelRepository;

    public DataSeeder(UsuarioRepository usuarioRepository,
                      ReservaVooRepository reservaVooRepository,
                      ReservaHotelRepository reservaHotelRepository) {
        this.usuarioRepository = usuarioRepository;
        this.reservaVooRepository = reservaVooRepository;
        this.reservaHotelRepository = reservaHotelRepository;
    }

    @Override
    public void run(String... args) {
        reservaVooRepository.deleteAll();
        reservaHotelRepository.deleteAll();
        usuarioRepository.deleteAll();

        Usuario demoUser = criarUsuario(
                "Cliente Demo",
                "cliente.demo@example.com",
                "11987654321",
                "12345678900"
        );

        criarReservaVoo(
                demoUser,
                "GranAir",
                "GRU",
                "LIS",
                LocalDateTime.now().plusDays(30),
                new BigDecimal("3500.00")
        );

        criarReservaHotel(
                demoUser,
                "Gran Resort Lisboa",
                "Lisboa",
                LocalDate.now().plusDays(30),
                LocalDate.now().plusDays(37),
                new BigDecimal("4200.00")
        );
    }

    private Usuario criarUsuario(String nome, String email, String telefone, String cpf) {
        Usuario usuario = new Usuario();
        usuario.setId(UUID.randomUUID().toString());
        usuario.setNome(nome);
        usuario.setEmail(email);
        usuario.setTelefone(telefone);
        usuario.setCpf(cpf);
        return usuarioRepository.save(usuario);
    }

    private void criarReservaVoo(Usuario usuario,
                                 String companhia,
                                 String origem,
                                 String destino,
                                 LocalDateTime partida,
                                 BigDecimal preco) {
        ReservaVoo reserva = new ReservaVoo();
        reserva.setId(UUID.randomUUID().toString());
        reserva.setUsuarioId(usuario.getId());
        reserva.setUsuarioCpf(usuario.getCpf());
        reserva.setCompanhiaAerea(companhia);
        reserva.setOrigem(origem);
        reserva.setDestino(destino);
        reserva.setDataPartida(partida);
        reserva.setPreco(preco);
        reserva.setStatus(ReservaVoo.StatusReserva.CONFIRMADA);
        reservaVooRepository.save(reserva);
    }

    private void criarReservaHotel(Usuario usuario,
                                   String nomeHotel,
                                   String localizacao,
                                   LocalDate checkIn,
                                   LocalDate checkOut,
                                   BigDecimal preco) {
        ReservaHotel hotel = new ReservaHotel();
        hotel.setId(UUID.randomUUID().toString());
        hotel.setUsuarioId(usuario.getId());
        hotel.setUsuarioCpf(usuario.getCpf());
        hotel.setNomeHotel(nomeHotel);
        hotel.setLocalizacao(localizacao);
        hotel.setDataCheckIn(checkIn);
        hotel.setDataCheckOut(checkOut);
        hotel.setPrecoTotal(preco);
        hotel.setStatus(ReservaHotel.StatusReserva.CONFIRMADA);
        reservaHotelRepository.save(hotel);
    }
}
