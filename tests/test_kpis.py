"""Pruebas del cuadro de mando ejecutivo.

El README promete «24 indicadores que cuadran entre si». Un cuadro de mando en
el que el margen no sale de dividir el beneficio entre los ingresos es peor que
no tener cuadro de mando: se toman decisiones con el. Aqui se comprueba cada
identidad contable, y que los desgloses por segmento y por canal suman el total.
"""

import numpy as np
import pytest

from generate_data import (
    CHANNELS,
    N_MONTHS,
    SEGMENTS,
    build_by_channel,
    build_by_segment,
    build_marketing,
    build_pipeline,
    build_summary,
)


@pytest.fixture(scope="module")
def resumen():
    np.random.seed(42)
    return build_summary()


@pytest.fixture(scope="module")
def por_segmento(resumen):
    return build_by_segment(resumen)


@pytest.fixture(scope="module")
def por_canal(resumen):
    return build_by_channel(resumen)


class TestForma:
    def test_hay_una_fila_por_mes(self, resumen):
        assert len(resumen) == N_MONTHS

    def test_son_veinticuatro_columnas_como_dice_el_readme(self, resumen):
        """La cifra publicada tiene que salir del codigo, no de la memoria."""
        assert len(resumen.columns) == 24

    def test_los_meses_van_en_orden_y_sin_repetirse(self, resumen):
        meses = list(resumen["month"])
        assert meses == sorted(meses)
        assert len(set(meses)) == len(meses)

    def test_los_meses_tienen_formato_anio_mes(self, resumen):
        for m in resumen["month"]:
            anio, mes = m.split("-")
            assert len(anio) == 4 and len(mes) == 2
            assert 1 <= int(mes) <= 12

    def test_no_falta_ningun_dato(self, resumen):
        assert not resumen.isna().any().any()


class TestIdentidadesContables:
    def test_el_margen_bruto_es_beneficio_entre_ingresos(self, resumen):
        esperado = resumen["gross_profit"] / resumen["revenue"]
        assert np.allclose(resumen["gross_margin_pct"], esperado, atol=1e-4)

    def test_el_margen_ebitda_es_ebitda_entre_ingresos(self, resumen):
        esperado = resumen["ebitda"] / resumen["revenue"]
        assert np.allclose(resumen["ebitda_margin_pct"], esperado, atol=1e-4)

    def test_el_arr_son_doce_veces_el_mrr(self, resumen):
        assert np.allclose(resumen["arr"], resumen["mrr"] * 12)

    def test_en_saas_el_mrr_es_el_ingreso_del_mes(self, resumen):
        assert np.allclose(resumen["mrr"], resumen["revenue"])

    def test_el_ebitda_no_supera_al_beneficio_bruto(self, resumen):
        """El EBITDA sale de restar los gastos operativos: no puede ser mayor."""
        assert (resumen["ebitda"] <= resumen["gross_profit"]).all()

    def test_el_beneficio_bruto_no_supera_al_ingreso(self, resumen):
        assert (resumen["gross_profit"] <= resumen["revenue"]).all()

    def test_la_relacion_ltv_cac_es_el_cociente(self, resumen):
        esperado = resumen["ltv"] / resumen["cac"].clip(1)
        assert np.allclose(resumen["ltv_cac_ratio"], esperado, atol=0.01)

    def test_la_cobertura_de_pipeline_es_pipeline_entre_ingresos(self, resumen):
        esperado = resumen["pipeline_value"] / resumen["revenue"].clip(1)
        assert np.allclose(resumen["pipeline_coverage"], esperado, atol=0.01)


class TestRangosCreibles:
    def test_ningun_indicador_monetario_es_negativo(self, resumen):
        for col in ("revenue", "gross_profit", "mrr", "arr", "marketing_spend",
                    "expansion_revenue", "pipeline_value", "cac", "ltv"):
            assert (resumen[col] >= 0).all(), f"{col} sale negativo"

    def test_los_porcentajes_estan_entre_cero_y_uno(self, resumen):
        for col in ("gross_margin_pct", "churn_rate", "win_rate"):
            assert resumen[col].between(0, 1).all(), f"{col} se sale de [0, 1]"

    def test_el_nrr_se_queda_dentro_de_su_banda(self, resumen):
        assert resumen["nrr"].between(0.7, 1.4).all()

    def test_la_tasa_de_exito_comercial_no_se_dispara(self, resumen):
        assert resumen["win_rate"].between(0.05, 0.6).all()

    def test_el_ciclo_de_venta_dura_al_menos_veinte_dias(self, resumen):
        assert (resumen["sales_cycle_days"] >= 20).all()

    def test_el_embudo_se_estrecha(self, resumen):
        """No se puede cerrar mas clientes que oportunidades cualificadas."""
        assert (resumen["sqls"] <= resumen["mqls"]).all()
        assert (resumen["new_customers"] <= resumen["sqls"]).all()

    def test_no_se_pierden_mas_clientes_de_los_que_entran(self, resumen):
        assert (resumen["churned_customers"] <= resumen["new_customers"]).all()

    def test_los_ingresos_no_bajan_del_suelo(self, resumen):
        assert (resumen["revenue"] >= 300_000).all()


class TestDesgloses:
    def test_hay_una_fila_por_segmento_y_mes(self, por_segmento):
        assert len(por_segmento) == len(SEGMENTS) * N_MONTHS
        assert set(por_segmento["segment"]) == set(SEGMENTS)

    def test_hay_una_fila_por_canal_y_mes(self, por_canal):
        assert len(por_canal) == len(CHANNELS) * N_MONTHS
        assert set(por_canal["channel"]) == set(CHANNELS)

    def test_los_segmentos_suman_el_ingreso_total(self, resumen, por_segmento):
        """Las cuotas se normalizan, asi que el reparto es exacto salvo redondeo."""
        suma = por_segmento.groupby("month")["revenue"].sum().sort_index()
        total = resumen.set_index("month")["revenue"].sort_index()
        # Cada segmento redondea a la unidad: hasta tres euros de diferencia.
        assert (abs(suma - total) <= len(SEGMENTS)).all()

    def test_los_canales_reparten_casi_todo_el_ingreso(self, resumen, por_canal):
        """Aqui las cuotas NO se normalizan: el ruido deja un margen pequeño."""
        suma = por_canal.groupby("month")["revenue"].sum().sort_index()
        total = resumen.set_index("month")["revenue"].sort_index()
        desvio = (suma - total).abs() / total
        assert (desvio < 0.05).all(), "el reparto por canal se aleja mas de un 5 %"

    def test_el_ticket_medio_es_ingreso_entre_clientes(self, por_segmento):
        esperado = por_segmento["revenue"] / por_segmento["new_customers"].clip(lower=1)
        assert np.allclose(por_segmento["avg_deal_size"], esperado, atol=0.01)

    def test_captar_por_outbound_cuesta_mas_que_por_inbound(self, por_canal):
        medias = por_canal.groupby("channel")["cac"].mean()
        assert medias["Outbound"] > medias["Inbound"]
        assert medias["Direct"] < medias["Inbound"]

    def test_ningun_desglose_trae_ingresos_negativos(self, por_segmento, por_canal):
        assert (por_segmento["revenue"] >= 0).all()
        assert (por_canal["revenue"] >= 0).all()


class TestMarketingYPipeline:
    def test_las_conversiones_del_embudo_son_cocientes(self, resumen):
        m = build_marketing(resumen)
        assert np.allclose(m["mql_to_sql_rate"], m["sqls"] / m["mqls"].clip(1), atol=1e-4)
        assert np.allclose(m["sql_to_won_rate"],
                           m["new_customers"] / m["sqls"].clip(1), atol=1e-4)

    def test_el_coste_por_lead_y_el_roas(self, resumen):
        m = build_marketing(resumen)
        assert np.allclose(m["cpl"], m["marketing_spend"] / m["mqls"].clip(1), atol=0.01)
        assert np.allclose(m["roas"], resumen["revenue"] / m["marketing_spend"].clip(1),
                           atol=0.01)

    def test_las_conversiones_no_pasan_del_cien_por_cien(self, resumen):
        m = build_marketing(resumen)
        assert m["mql_to_sql_rate"].between(0, 1).all()
        assert m["sql_to_won_rate"].between(0, 1).all()

    def test_el_pipeline_tiene_cinco_etapas_cada_mes(self, resumen):
        p = build_pipeline(resumen)
        assert len(p) == 5 * N_MONTHS
        assert p.groupby("month")["stage"].nunique().eq(5).all()

    def test_ninguna_etapa_esta_vacia_ni_en_negativo(self, resumen):
        p = build_pipeline(resumen)
        assert (p["deals"] >= 1).all()
        assert (p["value"] > 0).all()

    def test_hay_mas_valor_al_principio_del_embudo_que_al_final(self, resumen):
        p = build_pipeline(resumen)
        medias = p.groupby("stage")["value"].mean()
        assert medias["Prospecting"] > medias["Closed Won"]
