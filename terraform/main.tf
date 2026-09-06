# Локальный ресурс - просто создает файл с IP-адресом
resource "local_file" "vm_ip" {
  content  = "127.0.0.1"
  filename = "${path.module}/vm_ip.txt"
}

# Локальный ресурс - создает файл с SSH-командой
resource "local_file" "ssh_command" {
  content  = "ssh localhost"
  filename = "${path.module}/ssh_command.txt"
}