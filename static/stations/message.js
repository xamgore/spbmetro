Vue.component('message', {
  props: ['msg', 'subway', 'stationToColor'],
  computed: {
    date() {
      return (this.msg.date && moment.unix(this.msg.date).format("D MMM YY, HH:MM"))
    },
    text() {
      let offset = 0;
      let text = this.msg.text;

      this.msg.spans.forEach(([l, r], idx) => {
        let color = 'badge' + {
          'синяя': '-primary',
          'зелёная': '-success',
          'оранжевая': '-warning',
          'красная': '-danger',
          'фиолетовая': '-info',
          false: '',
        }[this.stationToColor[this.msg.stations[idx]]];

        let size = text.length;
        text = `${text.substring(0, l + offset)}<button type="button" class="btn badge mb-1 badge-light"><span class="badge badge-pill station ${color}"></span> ${ text.substring(l + offset, r + offset) }</button>${text.substring(r + offset)}`;
        offset += text.length - size;
      });

      return text;
    },
    stations() {
      return this.subway
        .filter(st => this.msg.stations.includes(st.name))
    },
  },
  template: `
    <div class="message">
      <div class="card">
        <div class="card-body">
          <p class="card-text" v-html="text"></p>
        </div>
      </div>
      
      <small class="id" :id="msg.message_id" :data-date="date">{{ msg.message_id }}</small>
    </div>
    `
});
