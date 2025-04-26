# 使用基础镜像
FROM ubuntu:20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive \
    SHADOWSOCKS_PASSWORD=xjq \
    SHADOWSOCKS_PORT=8388 \
    SHADOWSOCKS_CIPHER=aes-256-gcm \
    SHADOWSOCKS_PROTOCOL=origin \
    SHADOWSOCKS_OBFS=plain \
    SHADOWSOCKS_VERSION=libev \
    LIBEV_OBFS=n

# 安装依赖
RUN apt-get update && \
    apt-get install -y \
    gettext build-essential unzip gzip python3 python3-dev python3-setuptools curl openssl libssl-dev \
    autoconf  automake libtool gcc make perl cpio libpcre3 libpcre3-dev zlib1g-dev libev-dev libc-ares-dev git qrencode \
    libsodium-dev libmbedtls-dev wget \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 shadowsocks-libev
RUN wget --no-check-certificate -qO- https://api.github.com/repos/shadowsocks/shadowsocks-libev/releases/latest | grep 'tag_name' | cut -d\" -f4 | cut -c2- | xargs -I {} wget -qO- https://github.com/shadowsocks/shadowsocks-libev/releases/download/v{}/shadowsocks-libev-{}.tar.gz | tar xz && \
    cd shadowsocks-libev-* && \
    ./configure --disable-documentation && \
    make && make install && \
    cd .. && rm -rf shadowsocks-libev-*

# 配置 shadowsocks-libev
RUN mkdir -p /etc/shadowsocks-libev && \
    cat > /etc/shadowsocks-libev/config.json <<-EOF
{
    "server": ["[::0]", "0.0.0.0"],
    "server_port": ${SHADOWSOCKS_PORT},
    "password": "${SHADOWSOCKS_PASSWORD}",
    "timeout": 300,
    "user": "nobody",
    "method": "${SHADOWSOCKS_CIPHER}",
    "fast_open": false,
    "nameserver": "1.0.0.1",
    "mode": "tcp_and_udp"
}
EOF

# 安装 simple-obfs（如果需要）
RUN if [ "$LIBEV_OBFS" = "y" ]; then \
        git clone https://github.com/shadowsocks/simple-obfs.git && \
        cd simple-obfs && \
        git submodule update --init --recursive && \
        ./autogen.sh && \
        ./configure && \
        make && make install && \
        cd .. && rm -rf simple-obfs && \
        sed -i "/\"mode\":/a \"plugin\": \"obfs-server\",\n    \"plugin_opts\": \"obfs=${SHADOWSOCKS_OBFS}\"," /etc/shadowsocks-libev/config.json; \
    fi

# 暴露端口
EXPOSE ${SHADOWSOCKS_PORT}/tcp ${SHADOWSOCKS_PORT}/udp

# 启动 shadowsocks-libev
CMD ["/usr/local/bin/ss-server", "-c", "/etc/shadowsocks-libev/config.json"]