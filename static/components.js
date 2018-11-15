Vue.component('message', {
  props: ['event', 'station'],
  computed: {
    date() {return (this.event.date && moment.unix(this.event.date).format("D MMM, HH:MM"))},
    status() {return this.event.status || {}},
  },
  template: `
      <div class="card">
        <div class="card-body">
        
          <div style="display:flex; flex-direction: row; justify-content: space-between">
            <div>
              <h3 class="card-title">{{ event.message_id }}</h3>
              <h6 class="card-subtitle mb-3 text-muted">{{ date }}</h6>
            </div>
            
            <div>
              <station v-if="station" :station="station"></station>
            </div>
          </div>
          
          <p class="card-text">{{ event.text }}</p>
        </div>
      </div>
    `
});


Vue.component('station', {
  props: ['station'],
  computed: {
    color() {
      return 'badge' + {
        'синяя': '-primary',
        'зелёная': '-success',
        'оранжевая': '-warning',
        'красная': '-danger',
        'фиолетовая': '-info',
        false: '',
      }[this.station.line.color]
    },
  },
  template: `
      <button type="button" @click="$emit('choose', station)" @press.enter="$emit('choose', station)" 
              class="btn badge mb-1 badge-light" style="margin-right: 0.4rem">
        <span class="badge badge-pill station" :class="color"></span>
        {{ station.name }}
      </button>
    `
});


Vue.component('branch', {
  props: ['stations'],
  template: `
      <div>
        <station v-for="st in stations" :key="st.name" :station="st"
           @choose="$emit('choose', $event)" style="font-size: 85%" ></station>
      </div>
    `
});
