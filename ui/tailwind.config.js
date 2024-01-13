module.exports = {
    content: ['./src/**/*.{vue,js,ts}'],
    daisyui: {
      themes: ["light", "dark", "aqua"],
    },
    theme: {
      extend: {
        maxWidth: {
          '1/4': '25%',
          '1/2': '300px',
          '3/4': '75%',
          '9/10': '90%'
        },
        height: {
          '128': '32rem',
          '256': '50rem'
        },
        width: {
          '128': '32rem',
          '256': '50rem'
        },
        margin: {
          '9/10': '90%'
        }
      }
    }
  };