package br.edu.ibmec.services;
import br.edu.ibmec.dto.historicoconversadto;

public interface historicoconversaservices {

    void criarHistoricoConversa(historicoconversadto historico);
    historicoconversadto obterHistoricoConversaPorId(Long id);
    historicoconversadto salvarHistoricoConversa(historicoconversadto historico);
    historicoconversadto atualizarHistoricoConversa(Long id, historicoconversadto historico);
    void deletarHistoricoConversa(Long id);

}
