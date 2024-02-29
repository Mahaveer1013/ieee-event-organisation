particlesJS("particles-js", {
    particles: {
        number: { value: 150 },
        color: { value: "#800080" },
        shape: {
            type: "polygon",
            options: {
                polygon: {
                    nb_sides: 8,
                },
            },
        },
        opacity: { value: 0.6, random: true },
        size: { value: 6, random: true },
        move: {
            enable: true,
            speed: 5,
            direction: "center",
            random: false,
        },
    },
    interactivity: {
        events: {
            onhover: {
                enable: true,
                mode: "repulse",
            },
        },
    },
});
