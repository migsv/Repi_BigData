package br.edu.ibmec.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

import com.azure.cosmos.CosmosClientBuilder;
import com.azure.spring.data.cosmos.config.AbstractCosmosConfiguration;
import com.azure.spring.data.cosmos.config.CosmosConfig;
import com.azure.spring.data.cosmos.repository.config.EnableCosmosRepositories;


@Configuration
@EnableConfigurationProperties(CosmosProperties.class)
@PropertySource("classpath:application.properties")
@EnableCosmosRepositories(basePackages = "br.edu.ibmec.repository")
public class CosmosConfiguration extends AbstractCosmosConfiguration {
    private CosmosProperties cosmosProperties;

    public CosmosConfiguration(CosmosProperties cosmosProperties) {
        super();
        this.cosmosProperties = cosmosProperties;
    }

    @Bean 
    public CosmosClientBuilder cosmosClientBuilder() {
        return new CosmosClientBuilder()
            .endpoint(cosmosProperties.getUri())
            .key(cosmosProperties.getKey());
    }

    @Bean public CosmosConfig cosmosConfig() {
        return CosmosConfig.builder().build();
    }

    @Override
    protected String getDatabaseName() {
        return cosmosProperties.getDatabase();
    }
    
}