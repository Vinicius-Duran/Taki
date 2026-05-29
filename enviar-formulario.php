<?php
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'message' => 'Método não permitido.']);
    exit;
}

$destinatarios = [
    'contato@takirastreadores.com.br',
    'paulo@takirastreadores.com.br',
];

$honeypot = trim((string) ($_POST['website'] ?? ''));
if ($honeypot !== '') {
    echo json_encode(['ok' => true, 'message' => 'Mensagem enviada com sucesso.']);
    exit;
}

$nome = trim((string) ($_POST['nome'] ?? ''));
$empresa = trim((string) ($_POST['empresa'] ?? ''));
$telefone = trim((string) ($_POST['telefone'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$veiculos = trim((string) ($_POST['veiculos'] ?? ''));
$servico = trim((string) ($_POST['servico'] ?? ''));
$cidade = trim((string) ($_POST['cidade'] ?? ''));
$mensagem = trim((string) ($_POST['mensagem'] ?? ''));
$origem = trim((string) ($_POST['origem'] ?? 'site'));
$lgpd = isset($_POST['lgpd']) && ($_POST['lgpd'] === '1' || $_POST['lgpd'] === 'on');

if ($nome === '' || $empresa === '' || $telefone === '') {
    http_response_code(400);
    echo json_encode(['ok' => false, 'message' => 'Preencha nome, empresa e telefone.']);
    exit;
}

if (strpos($origem, 'contato') !== false && !$lgpd) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'message' => 'É necessário aceitar o contato conforme a política de privacidade.']);
    exit;
}

if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'message' => 'Informe um e-mail válido.']);
    exit;
}

$assunto = 'Novo lead — Takí Rastreadores (' . $origem . ')';

$linhas = [
    'Nova solicitação pelo site',
    '---------------------------',
    'Origem: ' . $origem,
    'Nome: ' . $nome,
    'Empresa: ' . $empresa,
    'Telefone: ' . $telefone,
];

if ($email !== '') {
    $linhas[] = 'E-mail: ' . $email;
}
if ($veiculos !== '') {
    $linhas[] = 'Veículos: ' . $veiculos;
}
if ($servico !== '') {
    $linhas[] = 'Serviço: ' . $servico;
}
if ($cidade !== '') {
    $linhas[] = 'Cidade: ' . $cidade;
}
if ($mensagem !== '') {
    $linhas[] = 'Mensagem: ' . $mensagem;
}

$linhas[] = 'Enviado em: ' . date('d/m/Y H:i:s');
$corpo = implode("\n", $linhas);

$from = 'noreply@takirastreadores.com.br';
$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "From: Takí Rastreadores <{$from}>\r\n";
if ($email !== '') {
    $headers .= 'Reply-To: ' . $email . "\r\n";
}

$enviado = false;
foreach ($destinatarios as $para) {
    if (@mail($para, $assunto, $corpo, $headers)) {
        $enviado = true;
    }
}

if (!$enviado) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'message' => 'Não foi possível enviar agora. Tente pelo WhatsApp ou telefone.']);
    exit;
}

echo json_encode(['ok' => true, 'message' => 'Mensagem enviada! Entraremos em contato em até 1 hora útil.']);
