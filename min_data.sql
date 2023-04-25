INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (1, 'Vue globale', 'fab fa-dashcube', '', 1, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (2, 'Grand livre', 'fas fa-book', 'grand_livre/', 3, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (3, 'Journal', 'fas fa-newspaper', null, 4, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (4, 'Ecriture', 'fas fa-feather-alt', 'journal/choix', 1, 3);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (5, 'Type', 'fas fa-th', 'journal/lister', 2, 3);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (6, 'Plan Comptable', 'fas fa-code-branch', null, 5, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (7, 'Compte général', 'fas fa-globe-africa', 'compte_general/lister', 1, 6);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (8, 'Compte tiers', 'fas fa-network-wired', 'compte_tiers/lister', 2, 6);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (9, 'Divers', 'fas fa-cogs', null, 6, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (10, 'Devise', 'fas fa-money-bill-wave', 'devise/lister', 1, 9);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (11, 'Devise équivalente', 'fas fa-coins', 'devise_equivalente/lister', 2, 9);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (12, 'Historique Société', 'fas fa-landmark', 'societe/', 4, 9);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (13, 'Balance', 'fas fa-balance-scale', 'balance/', 2, null);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (14, 'Pièce', 'fas fa-puzzle-piece', 'piece/lister', 3, 3);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (15, 'Exercice', 'fas fa-hourglass-half', 'exercice/lister', 3, 3);
INSERT INTO comptable_menu (id, name, icon, url, "order", parent_id) VALUES (16, 'Status d''entreprise', 'fas fa-gavel', 'status/lister', 3, 9);

INSERT INTO comptable_statusentreprise (id, nom, sigle) VALUES (1, 'Société Anonyme', 'SA');

INSERT INTO comptable_devise (id, code, nom) VALUES (1, 'MGA', 'Ariary');
INSERT INTO comptable_devise (id, code, nom) VALUES (2, 'EUR', 'Euro');
INSERT INTO comptable_devise (id, code, nom) VALUES (3, 'USD', 'Dollar');

INSERT INTO comptable_historiquesociete (id, nom, logo, objectif, siege, date_creation, nif, scan_nif, stat, scan_stat, reg_commerce, scan_reg_commerce, date_information, devise_compte_id, status_entreprise_id) VALUES (1, 'Dimpex', 'logo.png', 'La DIMPEX  (Dago Import Export) a pour objet social la production d''articles industriels et la vente de marchandises auprès de ces clients locaux et étrangers', 'ENCEINTE ITU ANDOHARANOFOTSY BP 1960 Antananarivo 101', '1672531200000', 'NIF-1234', '', 'STAT-1234', '', 'REG-1234', '', '1680566400000', 1, 1);

