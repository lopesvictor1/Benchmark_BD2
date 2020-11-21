# Benchmark_BD2



falar que tem que ir no arquivo /etc/default/influxdb e colocar a linha INFLUXDB_DATA_MAX_SERIES_PER_DATABASE=10000000 para funcionar inserções de mais de 1 milhão de linhas (nesse caso o máximo é 10 milhões)