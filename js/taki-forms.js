(function () {
  function statusEl(form) {
    var el = form.querySelector('.taki-form-status');
    if (!el) {
      el = document.createElement('p');
      el.className = 'taki-form-status';
      el.setAttribute('role', 'status');
      el.setAttribute('aria-live', 'polite');
      var submit = form.querySelector('[type="submit"], .form-submit, .btn-submit');
      if (submit && submit.parentNode) {
        submit.parentNode.insertBefore(el, submit);
      } else {
        form.appendChild(el);
      }
    }
    return el;
  }

  function fieldValue(form, name) {
    var el = form.querySelector('[name="' + name + '"]');
    if (!el) return '';
    if (el.type === 'checkbox') return el.checked ? '1' : '';
    return (el.value || '').trim();
  }

  function validate(form) {
    var required = form.querySelectorAll('[data-required]');
    for (var i = 0; i < required.length; i++) {
      var el = required[i];
      var val = el.type === 'checkbox' ? el.checked : (el.value || '').trim();
      if (!val) {
        el.focus();
        return 'Preencha todos os campos obrigatórios.';
      }
    }
    var lgpd = form.querySelector('[name="lgpd"]');
    if (lgpd && lgpd.hasAttribute('data-required') && !lgpd.checked) {
      lgpd.focus();
      return 'Aceite a política de privacidade para continuar.';
    }
    return '';
  }

  function bindForm(form) {
    if (form.dataset.takiBound === '1') return;
    form.dataset.takiBound = '1';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = validate(form);
      var status = statusEl(form);
      if (err) {
        status.textContent = err;
        status.className = 'taki-form-status taki-form-status--error';
        return;
      }

      var submitBtn = form.querySelector('[type="submit"], .form-submit, .btn-submit');
      var prevHtml = submitBtn ? submitBtn.innerHTML : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Enviando...';
      }
      status.textContent = '';
      status.className = 'taki-form-status';

      var data = new FormData(form);
      if (!data.get('origem')) {
        data.set('origem', form.getAttribute('data-origem') || document.title || 'site');
      }

      fetch(form.getAttribute('action') || 'enviar-formulario.php', {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          return res.json().then(function (body) {
            return { ok: res.ok && body.ok, message: body.message || 'Erro ao enviar.' };
          });
        })
        .catch(function () {
          return { ok: false, message: 'Falha na conexão. Tente novamente ou use o WhatsApp.' };
        })
        .then(function (result) {
          if (result.ok) {
            var origem = encodeURIComponent(data.get('origem') || form.getAttribute('data-origem') || 'site');
            window.location.href = 'obrigado.html?origem=' + origem;
            return;
          }
          status.textContent = result.message;
          status.className = 'taki-form-status taki-form-status--error';
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = prevHtml;
          }
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.taki-lead-form').forEach(bindForm);
  });
})();
