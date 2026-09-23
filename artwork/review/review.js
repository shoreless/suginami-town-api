const $ = id => document.getElementById(id);
const pct = n => `${n * 100}%`;
const hours = {morning: 8, midday: 12, evening: 18, night: 22};
let config;
function picture(path, className, alt) {
  const image = document.createElement('img');
  image.src = `../${path}`; image.className = className; image.alt = alt;
  image.decoding = 'async';
  image.addEventListener('error', () => {
    image.hidden = true;
    $('status').textContent = `An artwork file could not load: ${path}. Rebuild the catalogue if sources have changed.`;
  });
  return image;
}
function update() {
  document.documentElement.style.setProperty('--scale', Number($('scale').value) / 100);
  $('scale-value').value = `${$('scale').value}%`;
  document.body.classList.toggle('hide-character', !$('character').checked);
  document.body.classList.toggle('hide-information', !$('information').checked);
  document.body.classList.toggle('guides', $('guides').checked);
  const locale = $('locale').value === 'ja' ? 'ja-JP' : 'en-GB';
  const time = $('clock').value === 'live' ? new Date() : new Date(2026, 8, 23, hours[$('phase').value], 42);
  for (const clock of document.querySelectorAll('.clock')) clock.textContent = new Intl.DateTimeFormat(locale, {hour: '2-digit', minute: '2-digit', hour12: false}).format(time);
  for (const date of document.querySelectorAll('.date')) date.textContent = new Intl.DateTimeFormat(locale, {weekday: 'short', day: 'numeric', month: 'short'}).format(time);
  for (const weather of document.querySelectorAll('.weather')) { weather.hidden = !$('weather').checked; weather.textContent = locale === 'ja-JP' ? '晴れ · 24°（見本）' : 'Clear · 24° (sample)'; }
}
function render() {
  const scene = config.scenes.find(item => item.id === $('area').value);
  const phase = $('phase').value;
  const moment = scene.phases[phase];
  const section = document.createElement('section'); section.className = 'scene-section';
  const heading = document.createElement('div'); heading.className = 'scene-heading';
  const name = document.createElement('h2'); name.textContent = scene.name.ja; name.lang = 'ja';
  const description = document.createElement('p'); description.textContent = `${scene.name.en} / ${phase}`;
  heading.append(name, description); section.append(heading);
  const surfaces = document.createElement('div'); surfaces.className = 'surfaces';
  for (const [id, layout] of Object.entries(config.surfaces)) {
    const card = document.createElement('figure'); card.className = 'surface-card';
    const surface = document.createElement('div'); surface.className = `surface ${id}`;
    surface.dataset.scene = scene.id; surface.dataset.surface = id; surface.dataset.phase = phase;
    surface.style.aspectRatio = layout.aspect; surface.style.borderRadius = layout.radius;
    const background = moment.backgrounds[layout.background];
    if (background) {
      const backdrop = picture(background, 'backdrop', `${scene.name.ja} / ${scene.name.en} · ${phase} background`);
      backdrop.style.objectPosition = layout.focal_point.map(pct).join(' '); surface.append(backdrop);
      const scrim = document.createElement('div'); scrim.className = 'scrim'; surface.append(scrim);
      if (moment.character) {
        const character = picture(moment.character, 'character', moment.character_fallback ? 'Namisuke (evening character fallback)' : 'Namisuke');
        Object.assign(character.style, {left: pct(layout.character.x), bottom: pct(layout.character.bottom), width: pct(layout.character.width)});
        const shadow = document.createElement('div'); shadow.className = 'shadow';
        Object.assign(shadow.style, {left: pct(layout.character.x), bottom: pct(layout.character.bottom + .005), width: pct(layout.character.width * .7)});
        surface.append(shadow, character);
      }
      const info = document.createElement('div'); info.className = 'information';
      Object.assign(info.style, {left: pct(layout.information.x), top: pct(layout.information.y), width: pct(layout.information.width), textAlign: layout.information.align});
      const clock = document.createElement('time'); clock.className = 'clock'; clock.style.fontSize = `${layout.clock_size * 100}cqw`;
      const date = document.createElement('span'); date.className = 'date';
      const weather = document.createElement('span'); weather.className = 'weather';
      const place = document.createElement('div'); place.className = 'place-label';
      for (const language of config.typography.name_order) {
        const label = document.createElement('span'); label.className = `place-${language}`;
        label.lang = language; label.textContent = scene.name[language]; place.append(label);
      }
      info.append(clock, date, weather, place); surface.append(info);
    } else {
      surface.classList.add('missing');
      const missing = document.createElement('p'); missing.className = 'missing-label';
      missing.textContent = `${phase} · ${layout.background}\nArtwork not available yet`;
      surface.append(missing);
    }
    const caption = document.createElement('figcaption'); caption.textContent = layout.label;
    const ratio = document.createElement('span'); ratio.textContent = id === 'wide' ? '2:1' : '1:1'; caption.append(ratio);
    card.append(surface, caption); surfaces.append(card);
  }
  section.append(surfaces); $('scenes').replaceChildren(section);
  const summary = config.summary;
  $('status').textContent = `${summary.backgrounds_available} / ${summary.backgrounds_expected} backgrounds available · ${scene.name.ja} / ${scene.name.en} · ${phase} · ${moment.missing_backgrounds.length ? `Missing: ${moment.missing_backgrounds.join(', ')}` : 'Three composition previews'}${moment.character_fallback ? ' · Evening character fallback' : ''}`;
  $('character-status').textContent = moment.character_fallback ? `The ${phase} character variant is not available yet. This preview uses the approved evening character.` : moment.character ? `Character: ${moment.character.split('/').at(-1)}` : 'No character asset is available yet.';
  $('character-link').hidden = !moment.character;
  $('character-preview').hidden = !moment.character;
  if (moment.character) {
    $('character-link').href = `../${moment.character}`;
    $('character-preview').src = `../${moment.character}`;
  } else {
    $('character-preview').removeAttribute('src');
  }
  const url = new URL(location.href); url.searchParams.set('area', scene.id); url.searchParams.set('phase', phase);
  history.replaceState(null, '', url);
  update();
}
try {
  const response = await fetch('../layouts/collection.json');
  if (!response.ok) throw new Error(`Layout returned ${response.status}`);
  config = await response.json();
  document.documentElement.style.setProperty('--overlay-font', config.typography.family);
  document.documentElement.style.setProperty('--overlay-weight', config.typography.weight);
  document.documentElement.style.setProperty('--overlay-opacity', config.typography.opacity);
  for (const scene of config.scenes) {
    const option = document.createElement('option'); option.value = scene.id;
    option.textContent = `${scene.name.ja} / ${scene.name.en}`; $('area').append(option);
  }
  const query = new URLSearchParams(location.search);
  const area = query.get('area') || 'kugayama';
  if (config.scenes.some(scene => scene.id === area)) $('area').value = area;
  if (config.phase_order.includes(query.get('phase'))) $('phase').value = query.get('phase');
  $('area').disabled = false; $('phase').disabled = false;
  render();
  document.querySelector('.controls').addEventListener('input', event => ['area', 'phase'].includes(event.target.id) ? render() : update());
  setInterval(() => { if (!document.hidden && $('clock').value === 'live') update(); }, 1000);
} catch (error) { $('status').textContent = `Could not load the study. Run python3 artwork/scripts/build_catalogue.py, then serve the repository with python3 -m http.server 8000. ${error.message}`; }
