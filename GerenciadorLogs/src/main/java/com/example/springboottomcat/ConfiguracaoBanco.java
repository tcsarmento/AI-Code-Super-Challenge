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
	        dataSource.setDriverClassName("oracle.jdbc.OracleDriver");
	        dataSource.setUrl("jdbc:oracle:thin:@localhost:1521:orcl");
	        dataSource.setUsername("PRONAF");
	        dataSource.setPassword("PRONAF");
	        return dataSource;
	    }
		


		@Bean
		public JpaVendorAdapter jpaVendorAdapter(){
			HibernateJpaVendorAdapter adapter = new HibernateJpaVendorAdapter();
			adapter.setDatabase(Database.ORACLE);
			adapter.setShowSql(false);
			adapter.setGenerateDdl(false);
			adapter.setDatabasePlatform("org.hibernate.dialect.OracleDialect");
			adapter.setPrepareConnection(true);
			return adapter;
		}
}
