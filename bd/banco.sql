SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
-- Deletar banco e recriar do zero
DROP DATABASE IF EXISTS empresa;
CREATE DATABASE empresa;
USE empresa;

-- Tabela de Clientes (forçando AUTO_INCREMENT)
CREATE TABLE clientes(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- Tudo em uma linha
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    idade INT
);

CREATE TABLE pedidos(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- Tudo em uma linha
    cliente_id INT NOT NULL,
    produto VARCHAR(150) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Inserir dados dos clientes (SEM especificar ID)
INSERT INTO clientes (nome, email, idade) VALUES
('Ana Paula', 'anapaula@exemplo.com', 25),
('Bruno Silva', 'brunosilva@exemplo.com', 30),
('Carla Souza', 'carlasouza@exemplo.com', 28),
('Daniel Oliveira', 'danieloliveira@exemplo.com', 35),
('Elisa Mendes', 'elisamendes@exemplo.com', 27);

-- Verificar se IDs foram gerados
SELECT * FROM clientes;

-- Inserir dados dos pedidos (SEM especificar ID)
INSERT INTO pedidos (cliente_id, produto, valor) VALUES
(1, 'Notebook', 2500.00),
(2, 'Smartphone', 1500.00),
(1, 'Mouse', 50.00),
(3, 'Teclado', 100.00),
(4, 'Monitor', 800.00),
(2, 'Fone de Ouvido', 200.00);

-- Verificar se IDs foram gerados
SELECT * FROM pedidos;

-- Consulta de exemplo
SELECT c.nome AS cliente, p.produto, p.valor 
FROM clientes c 
JOIN pedidos p ON c.id = p.cliente_id;

-- Consulta total gasto por cliente
SELECT c.nome, SUM(p.valor) AS total_gasto 
FROM clientes c 
JOIN pedidos p ON c.id = p.cliente_id 
GROUP BY c.nome 
ORDER BY total_gasto DESC;
