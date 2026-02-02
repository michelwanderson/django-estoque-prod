document.addEventListener('DOMContentLoaded', () => {                                                                                  
    // Animação ao carregar a página para os elementos principais                                                                      
    const heroSection = document.querySelector('.hero');                                                                               
    const featureItems = document.querySelectorAll('.feature-item');                                                                   
    const navLinks = document.querySelectorAll('nav a');                                                                               
                                                                                                                                        
    // Animação do Hero                                                                                                                
    if (heroSection) {                                                                                                                 
        heroSection.style.opacity = '0';                                                                                               
        heroSection.style.transform = 'translateY(20px)';                                                                              
        setTimeout(() => {                                                                                                             
            heroSection.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';                                           
            heroSection.style.opacity = '1';                                                                                           
            heroSection.style.transform = 'translateY(0)';                                                                             
        }, 300);                                                                                                                       
    }                                                                                                                                  
                                                                                                                                        
    // Animação dos itens de Features com um pequeno atraso entre eles                                                                 
    featureItems.forEach((item, index) => {                                                                                            
        item.style.opacity = '0';                                                                                                      
        item.style.transform = 'scale(0.98)';                                                                                          
        setTimeout(() => {                                                                                                             
            item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';                                                  
            item.style.opacity = '1';                                                                                                  
            item.style.transform = 'scale(1)';                                                                                         
        }, 500 + index * 150);                                                                                                         
    });                                                                                                                                

    // Animação para itens de lista (Estoque, Histórico)
    const listItems = document.querySelectorAll('.item-list li');
    if (listItems.length > 0) {
        listItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-10px)';
            setTimeout(() => {
                item.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 300 + index * 100);
        });
    }
                                                                                                                                        
    // Efeito hover sutil nos links de navegação                                                                                       
    navLinks.forEach(link => {                                                                                                         
        link.addEventListener('mouseenter', () => {                                                                                    
            link.style.transform = 'scale(1.05)';                                                                                      
        });                                                                                                                            
        link.addEventListener('mouseleave', () => {                                                                                    
            link.style.transform = 'scale(1)';                                                                                         
        });                                                                                                                            
    });                                                                                                                                
                                                                                                                                        
    // Efeito no botão CTA ao passar o mouse                                                                                           
    const ctaButtons = document.querySelectorAll('.cta-button');
    ctaButtons.forEach(ctaButton => {
        ctaButton.addEventListener('mousemove', (e) => {
            const rect = ctaButton.getBoundingClientRect();
            const x = e.clientX - rect.left;                                                                                           
            const y = e.clientY - rect.top;                                                                                            
            ctaButton.style.backgroundImage = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.2), rgba(255,255,255,0))`;
        });                                                                                                                            
        ctaButton.addEventListener('mouseleave', () => {                                                                               
            ctaButton.style.backgroundImage = '';
        });                                                                                                                            
    });

    // Validação de Estoque (Página de Produção)
    const stockList = document.getElementById('stock-list');
    const productSelect = document.getElementById('id_produto');
    const quantityInput = document.getElementById('id_quantidade');
    const productionForm = document.querySelector('.hero form');

    if (stockList && productSelect && quantityInput && productionForm) {
        const stockMap = {};

        // Cria mapa de ID -> Quantidade disponível
        Array.from(stockList.children).forEach(li => {
            const id = li.dataset.id;
            // Garante que a quantidade seja um número (substitui vírgula por ponto se necessário)
            const qty = parseFloat(li.dataset.quantity.replace(',', '.'));
            if (id) stockMap[id] = qty;
        });

        productionForm.addEventListener('submit', (e) => {
            const selectedId = productSelect.value;
            const inputQty = parseFloat(quantityInput.value);

            if (selectedId && stockMap[selectedId] !== undefined) {
                const available = stockMap[selectedId];
                if (inputQty > available) {
                    e.preventDefault(); // Impede o envio
                    alert(`Quantidade indisponível! O estoque atual é de ${available}.`);
                    quantityInput.focus();
                    quantityInput.style.borderColor = '#e74c3c'; // Destaca o erro visualmente
                }
            }
        });
    }
});