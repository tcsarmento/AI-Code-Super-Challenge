package com.example.springboottomcat;

import javax.sql.DataSource;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaVendorAdapter;
import org.springframework.orm.jpa.vendor.Database;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;

@Configuration
public class ConfiguracaoBanco {
	
		@Bean
	    public DataSource dataSource(){
	        DriverManagerDataSource dataSource = new DriverManagerDataSource();
	        dataSource.setDriverClassName("org.postgresql.Driver");
	        dataSource.setUrl("jdbc:postgresql://localhost/postgres");
	        dataSource.setUsername("postgres");
	        dataSource.setPassword("root");
	        return dataSource;
	    }
		


		@Bean
		public JpaVendorAdapter jpaVendorAdapter(){
			HibernateJpaVendorAdapter adapter = new HibernateJpaVendorAdapter();
			adapter.setDatabase(Database.ORACLE);
			adapter.setShowSql(false);
			adapter.setGenerateDdl(true);
			adapter.setDatabasePlatform("org.hibernate.dialect.PostgreSQLDialect");
			adapter.setPrepareConnection(true);
			return adapter;
		}
}
