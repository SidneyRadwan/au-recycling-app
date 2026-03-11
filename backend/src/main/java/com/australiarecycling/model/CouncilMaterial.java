package com.australiarecycling.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "council_materials",
       uniqueConstraints = @UniqueConstraint(columnNames = {"council_id", "material_id"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CouncilMaterial {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "council_id")
    private Council council;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "material_id")
    private Material material;

    @Enumerated(EnumType.STRING)
    @Column(name = "bin_type", nullable = false, length = 50)
    private BinType binType;

    @Column(columnDefinition = "TEXT")
    private String instructions;

    @Column(columnDefinition = "TEXT")
    private String notes;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    public enum BinType {
        RECYCLING,
        GENERAL_WASTE,
        GREEN_WASTE,
        SOFT_PLASTICS,
        SPECIAL_DROP_OFF,
        NOT_ACCEPTED
    }
}
