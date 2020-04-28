<template>
  <span>
    <template v-if="source.published_at">
      <time class="d-none d-sm-inline-block" :datetime="source.published_at">
        {{ formatDate(source.published_at) }}
      </time>
      <time class="d-inline-block d-sm-none" :datetime="source.published_at">
        {{ formatDate(source.published_at, true) }}
      </time>
    </template>
    <a class="source_type text-secondary" :href="source.url" target="_blank">
      <img
        v-if="source.type == 'FACTCHECK_VLAANDEREN'"
        style="vertical-align: middle; max-height: 15px;"
        src="https://factcheck.vlaanderen/static/favicon/favicon-32x32.png"
        class="fc_flanders"
      />
      <vrt-icon v-else-if="source.type.startsWith('VRT')" />
      <nc-icon v-else-if="source.type.startsWith('NIEUWSCHECKERS')" />
      <img
        v-else-if="source.type.startsWith('KNACK')"
        src="https://www.knack.be/images/svg/logos/logo_Site-Knack-NL.svg?v4.2.3"
        class="knack-logo"
      />
      <template v-else>
        <img
          v-if="flemish(source.name)"
          src="https://www.vlaamsparlement.be/sites/all/themes/balance_theme/favicon.ico"
          class="f_parl"
        />
        <icon
          :class="`${source.type.toLowerCase()} text-context`"
          :name="source.type | pick_icon"
          size="xs"
        />
      </template>
      <icon
        v-if="source.type.startsWith('VRT')"
        class="url text-context"
        name="play-circle"
        size="xs"
      />
      <icon v-else class="url text-context" name="link" size="xs" />
    </a>
  </span>
</template>

<script>
import utilMixin from "@/mixins/utilMixin";
import VrtIcon from "@/assets/vrt.svg";
import NCIcon from "@/assets/nc.svg";

export default {
  name: "SourceIcon",
  props: ["source"],
  mixins: [utilMixin],
  components: {
    "vrt-icon": VrtIcon,
    "nc-icon": NCIcon,
  },
  methods: {
    flemish(source) {
      return source.includes("Flemish");
    },
  },
  filters: {
    pick_icon(source_type) {
      if (source_type == "TWITTER") {
        return "brands/twitter";
      }
      return "university";
    },
    flag(country) {
      if (country == "BE") {
        return "🇧🇪 ";
      }
      return "🇳🇱 ";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.source_type > svg,
.source_type > img {
  margin-left: 0.5rem;
}

.factchecked svg {
  width: 12px;
}

.factchecked svg.search {
  margin-right: 5px;
}

.factchecked svg.link {
  margin-left: 5px;
}

svg.twitter {
  color: #1da1f2;
}

tr svg.url {
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s 0.5s, opacity 0.5s linear;
  margin-right: -0.5rem;
}

tr:hover svg.url {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.5s linear;
}

.vrt_logo {
  max-width: 50px;
}

.nc_logo {
  height: 10px;
  max-width: 10px;
  margin-bottom: 5px;
}

img.knack-logo {
  max-width: 60px;
  margin-left: 10px;
  margin-bottom: 3px;
}

img.fc_flanders {
  vertical-align: middle;
  max-height: 15px;
}

img.f_parl {
  vertical-align: middle;
  max-height: 15px;
}
@media (max-width: 575px) {
  .info {
    margin-right: 10px;
  }
}
</style>
